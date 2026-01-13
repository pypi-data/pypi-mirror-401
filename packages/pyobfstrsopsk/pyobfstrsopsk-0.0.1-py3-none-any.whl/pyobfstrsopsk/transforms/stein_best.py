"""
Stein Best Obfuscator

Obfuscates imports by XORing module names with keys and renaming them to Japanese names.
Similar to reverse_strings but more comprehensive.
"""

import random
import string
from typing import Optional

import pyobfstrsopsk.ast_compat as ast
from pyobfstrsopsk.ast_annotation import add_parent
from pyobfstrsopsk.rename.name_generator import name_generator

# -------------------------------
# Helpers
# -------------------------------
CHINESE_KEYS = [
    '璞', '珮', '琪', '瑗', '琨', '瑜', '玮', '晗', '翔', '珂',
    '珍', '晟', '澜', '玺', '彤', '茗', '颢', '瑾', '璟', '翊'
]


def _rand_name(prefix="stein_", length=None) -> str:
    """Generate a random name using Japanese characters."""
    if length is None:
        length = random.randint(2, 5)
    
    # Extended Japanese character set
    japanese_chars = (
        # Basic Hiragana (46 characters)
        "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん" +
        # Hiragana dakuten/handakuten
        "がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ" +
        # Small hiragana
        "ぁぃぅぇぉゃゅょっ" +
        # Basic Katakana (46 characters)
        "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン" +
        # Katakana dakuten/handakuten
        "ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ" +
        # Small katakana
        "ァィゥェォャュョッ" +
        # Extended katakana
        "ヴヵヶ" +
        # Common Kanji (approx 500 characters)
        "日一月火水木金土人子父母男女学校学生先生本友達家食飲行来見聞話言語読書写紙画音楽休仕事故仕事電車車道駅店買売社員会社工場場市町村山川田海空雨花草木竹林森犬猫魚鳥虫名前上下左右前後中内外大小多少長高低新古白黒赤青黄安高早良い悪小中学校高校大学院図書館公園病院食品品物製品作品作物動物植物生物理科科学数学社会国語英語体育美術館室屋部局課係役員長官民法法律規則制度政策政治経済経営営業業者企業産業農業工業商業サービス仕事事事業活動動作動運動運転転回開閉出入退出入学卒業旅行旅館宿泊住宅住生活活生命令和昭和平成明治大正春夏秋冬東西南北都道府県市区町村山川海原島野里森田園地図世界国外国際関係平和戦争軍武器安全保障環境汚染地球温暖化自然災害地震台風洪水火山噴火津波被害救助支援協力団体組織機関委員会議会政府省庁官僚公務員議員選挙投票民主主義自由平等権利義務責任社会福祉医療健康保険年金老後介護障害者高齢者子供若者家族結婚離婚出生死亡葬式宗教信仰神仏寺神社教会祭典礼儀伝統文化芸術文学小説詩歌俳句短歌音楽楽器演奏歌唱舞踊演劇映画テレビ放送新聞雑誌出版報道情報通信インターネットコンピュータ技術科学研究開発実験データ分析統計調査結果報告論文学会発表特許権利著作権商標登録許可認証基準規格品質管理安全確認検査点検修理保守運用操作設定調整変更更新改良改善進歩発展成長拡大縮小減少増加変化変動変革改革革新創造発明発見解決対処対応処理実行実施実現達成成功失敗困難容易可能不可能必要十分不足過剰適切適当妥当正当正当化理由原因結果影響効果効率利益損失損害危険安全安心信頼信用名誉評判評価判断決定選択意思意思表示同意承諾拒否反対抗議主張要求請求申請申告報告連絡相談協議交渉折衝調整調停仲裁裁判訴訟法律違反犯罪被害加害者警察逮捕拘留勾留起訴判決刑罰執行服役釈放更生社会復帰就職雇用労働仕事職場職種業種企業会社組織団体組合"
    )
    
    return prefix + "".join(random.choice(japanese_chars) for _ in range(length))


def _rand_key() -> str:
    """Generate a random Chinese key."""
    return random.choice(CHINESE_KEYS)


def _xor_list(s: str, key) -> list[int]:
    """XOR a string with a key and return the list of integers."""
    key_ord = ord(key) if isinstance(key, str) else key
    return [ord(c) ^ key_ord for c in s]


def _encoded_expr_str(s: str, key, decoder_name: str) -> str:
    """Generate an encoded expression string using XOR."""
    key_ord = ord(key) if isinstance(key, str) else key
    xor_vals = _xor_list(s, key_ord)
    return f"{decoder_name}({repr(key)}, [{', '.join(map(str, xor_vals))}])"


# -------------------------------
# AST Transformer
# -------------------------------
class SteinBestObfuscator(ast.NodeTransformer):
    """Transformer that obfuscates import names."""
    
    def __init__(self, imports_map, protected_names: set, globals_set: set):
        self.imports = imports_map
        self.protected_names = protected_names  # Names that should not be renamed
        self.globals = globals_set
        self.scope_stack = [set()]

    def _is_shadowed(self, name: str) -> bool:
        """Check if a name is shadowed in the current scope."""
        return any(name in scope for scope in self.scope_stack)

    def _should_rename(self, name: str) -> bool:
        """Determine if a name should be renamed."""
        # Never rename globals or shadowed names
        if name in self.globals or self._is_shadowed(name):
            return False
        
        # Never rename protected names (annotations, decorators, etc.)
        if name in self.protected_names:
            return False
        
        # Otherwise, rename if it's in imports
        return name in self.imports

    def visit_FunctionDef(self, node):
        params = {arg.arg for arg in node.args.args}
        if getattr(node.args, "posonlyargs", None):
            params.update({a.arg for a in node.args.posonlyargs})
        if node.args.vararg:
            params.add(node.args.vararg.arg)
        if node.args.kwarg:
            params.add(node.args.kwarg.arg)
        
        self.scope_stack.append(params | {node.name})
        node.body = [self.visit(n) for n in node.body]
        self.scope_stack.pop()
        return node

    def visit_AsyncFunctionDef(self, node):
        return self.visit_FunctionDef(node)

    def visit_Lambda(self, node):
        params = {arg.arg for arg in node.args.args}
        if getattr(node.args, "posonlyargs", None):
            params.update({a.arg for a in node.args.posonlyargs})
        if node.args.vararg:
            params.add(node.args.vararg.arg)
        if node.args.kwarg:
            params.add(node.args.kwarg.arg)
        self.scope_stack.append(params)
        node.body = self.visit(node.body)
        self.scope_stack.pop()
        return node

    def visit_ClassDef(self, node):
        self.scope_stack[-1].add(node.name)
        self.scope_stack.append(set())
        
        # Rewrite class bases if they refer to renamed imports
        for i, base in enumerate(node.bases):
            if isinstance(base, ast.Name):
                base_name = base.id
                if self._should_rename(base_name):
                    node.bases[i] = ast.Name(id=self.imports[base_name][0], ctx=ast.Load())
            elif isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name):
                base_name = base.value.id
                if self._should_rename(base_name):
                    node.bases[i] = ast.Attribute(
                        value=ast.Name(id=self.imports[base_name][0], ctx=ast.Load()),
                        attr=base.attr,
                        ctx=ast.Load()
                    )
        
        node.body = [self.visit(n) for n in node.body]
        self.scope_stack.pop()
        return node

    def visit_With(self, node):
        if hasattr(node, 'items'):
            for item in node.items:
                if item.optional_vars and isinstance(item.optional_vars, ast.Name):
                    self.scope_stack[-1].add(item.optional_vars.id)
        else:
            if node.optional_vars and isinstance(node.optional_vars, ast.Name):
                self.scope_stack[-1].add(node.optional_vars.id)
        return self.generic_visit(node)

    def visit_For(self, node):
        target = node.target
        if isinstance(target, ast.Name):
            self.scope_stack[-1].add(target.id)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for elt in target.elts:
                if isinstance(elt, ast.Name):
                    self.scope_stack[-1].add(elt.id)
        return self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if node.name and isinstance(node.name, str):
            self.scope_stack[-1].add(node.name)
        return self.generic_visit(node)

    def visit_Assign(self, node):
        for t in node.targets:
            if isinstance(t, ast.Name):
                self.scope_stack[-1].add(t.id)
            elif isinstance(t, (ast.Tuple, ast.List)):
                for e in t.elts:
                    if isinstance(e, ast.Name):
                        self.scope_stack[-1].add(e.id)
        return self.generic_visit(node)

    def visit_AnnAssign(self, node):
        # Visit target to mark it as defined
        t = node.target
        if isinstance(t, ast.Name):
            self.scope_stack[-1].add(t.id)
        
        # Don't transform annotations (they're not executed at runtime in most cases)
        # Just visit the value
        if node.value:
            node.value = self.visit(node.value)
        
        return node

    def visit_Name(self, node):
        if self._should_rename(node.id):
            node.id = self.imports[node.id][0]
        return node


# -------------------------------
# Main function
# -------------------------------
def stein_best(module: ast.Module, seed: Optional[int] = None, safe_mode: bool = True) -> ast.Module:
    """
    Obfuscate imports in a module by XORing module names and renaming them.
    
    :param module: The AST module to obfuscate
    :param seed: Optional random seed for reproducibility
    :param safe_mode: If True, skip star imports for safety
    :return: The obfuscated AST module
    """
    if seed is not None:
        random.seed(seed)

    tree = module

    # -------------------------------
    # Top-level redefinition detection
    redefined: set[str] = set()
    
    class TopLevelRedefCollector(ast.NodeVisitor):
        def visit_FunctionDef(self, node): 
            redefined.add(node.name)
        def visit_AsyncFunctionDef(self, node): 
            redefined.add(node.name)
        def visit_ClassDef(self, node): 
            redefined.add(node.name)
        def visit_Assign(self, node):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    redefined.add(t.id)
                elif isinstance(t, (ast.Tuple, ast.List)):
                    for elt in t.elts:
                        if isinstance(elt, ast.Name):
                            redefined.add(elt.id)
        def visit_AnnAssign(self, node):
            t = node.target
            if isinstance(t, ast.Name):
                redefined.add(t.id)

    TopLevelRedefCollector().visit(tree)

    # -------------------------------
    # Hard decoder
    gen = name_generator()
    decoder_name = next(gen)
    decoder_src = f"""
def {decoder_name}(key, data):
    key_ord = ord(key) if isinstance(key, str) else key
    result = []
    for val in data:
        result.append(chr(val ^ key_ord))
    return ''.join(result)
"""

    # -------------------------------
    # Collect imports (safe, skips star-import expansion)
    imports = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                base = alias.asname or alias.name
                imports[base] = (_rand_name(), alias.name, None, "module")
        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue
            # avoid star imports for safety
            if any(alias.name == "*" for alias in node.names):
                continue
            for alias in node.names:
                imports[alias.asname or alias.name] = (_rand_name(), node.module, alias.name, "from")

    # remove imports that are redefined at top level
    imports = {k: v for k, v in imports.items() if k not in redefined}

    # -------------------------------
    # Collect names used in annotations (recursively)
    annotation_names = set()
    
    class AnnotationCollector(ast.NodeVisitor):
        def visit_arg(self, node):
            if node.annotation:
                self._collect_names(node.annotation)
            self.generic_visit(node)
        
        def visit_AnnAssign(self, node):
            if node.annotation:
                self._collect_names(node.annotation)
            # Don't visit the annotation in generic_visit, only the value
            if node.value:
                self.visit(node.value)
        
        def visit_FunctionDef(self, node):
            if node.returns:
                self._collect_names(node.returns)
            self.generic_visit(node)
        
        def visit_AsyncFunctionDef(self, node):
            if node.returns:
                self._collect_names(node.returns)
            self.generic_visit(node)
        
        def _collect_names(self, node):
            """Recursively collect all Name nodes from an annotation."""
            if isinstance(node, ast.Name):
                annotation_names.add(node.id)
            elif isinstance(node, ast.Subscript):
                # Handle generics like Set[str], Optional[X]
                # Check for ast.Index (Python < 3.9) - it may not exist in newer versions
                try:
                    if isinstance(node.slice, ast.Index):  # Python < 3.9
                        self._collect_names(node.slice.value)
                    else:
                        self._collect_names(node.slice)
                except (AttributeError, TypeError):
                    # ast.Index doesn't exist or slice is directly accessible
                    self._collect_names(node.slice)
                self._collect_names(node.value)
            elif isinstance(node, ast.Attribute):
                self._collect_names(node.value)
            elif isinstance(node, ast.Tuple):
                for elt in node.elts:
                    self._collect_names(elt)
            elif isinstance(node, ast.List):
                for elt in node.elts:
                    self._collect_names(elt)
            elif isinstance(node, ast.BinOp):
                # Handle Union types with | operator (Python 3.10+)
                self._collect_names(node.left)
                self._collect_names(node.right)
    
    AnnotationCollector().visit(tree)

    # -------------------------------
    # Collect decorator names (they're used at runtime!)
    decorator_names = set()
    
    class DecoratorCollector(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            for decorator in node.decorator_list:
                self._collect_names(decorator)
            self.generic_visit(node)
        
        def visit_AsyncFunctionDef(self, node):
            for decorator in node.decorator_list:
                self._collect_names(decorator)
            self.generic_visit(node)
        
        def visit_ClassDef(self, node):
            for decorator in node.decorator_list:
                self._collect_names(decorator)
            self.generic_visit(node)
        
        def _collect_names(self, node):
            """Collect names from decorator expressions."""
            if isinstance(node, ast.Name):
                decorator_names.add(node.id)
            elif isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name):
                    decorator_names.add(node.value.id)
            elif isinstance(node, ast.Call):
                # Decorator with arguments like @decorator(...)
                self._collect_names(node.func)
    
    DecoratorCollector().visit(tree)

    # -------------------------------
    # Collect globals
    globals_set = set()
    
    class GlobalCollector(ast.NodeVisitor):
        def visit_Global(self, node):
            globals_set.update(node.names)
        def visit_Nonlocal(self, node):
            globals_set.update(node.names)
    
    GlobalCollector().visit(tree)

    # -------------------------------
    # Protected names = annotations + decorators
    protected_names = annotation_names | decorator_names

    # -------------------------------
    # Build import stubs
    kept_nodes = [n for n in tree.body if not isinstance(n, (ast.Import, ast.ImportFrom))]
    stubs_src = [decoder_src]

    # Create obfuscated imports AND keep original names for protected names
    for name, (var, module, obj, kind) in imports.items():
        key = _rand_key()
        if kind == "module":
            stubs_src.append(f"{var} = __import__({_encoded_expr_str(module, key, decoder_name)})")
        else:
            stubs_src.append(
                f"{var} = getattr(__import__({_encoded_expr_str(module, key, decoder_name)}, fromlist=[{_encoded_expr_str(obj, key, decoder_name)}]), {_encoded_expr_str(obj, key, decoder_name)})"
            )
        
        # If this name is protected (used in annotations or decorators), create an alias
        if name in protected_names:
            stubs_src.append(f"{name} = {var}")

    # Add simple decoy assignments
    for _ in range(random.randint(3, 5)):
        n = _rand_name()
        stubs_src.append(f"{n} = 123 ^ 0")

    # Parse stubs
    stubs_nodes = []
    for line in stubs_src:
        try:
            parsed = ast.parse(line)
            stubs_nodes.extend(parsed.body)
        except Exception:
            pass

    # Transform rest of AST
    transformer = SteinBestObfuscator(imports, protected_names, globals_set)
    new_body = [transformer.visit(n) for n in kept_nodes]

    # Combine
    final_nodes = stubs_nodes + new_body
    final_tree = ast.Module(body=final_nodes, type_ignores=getattr(tree, 'type_ignores', []))
    ast.fix_missing_locations(final_tree)

    return final_tree


def stein_best_code(code: str, seed: Optional[int] = None, safe_mode: bool = True) -> str:
    """
    Obfuscate imports in Python source code by XORing module names and renaming them.
    
    This is a convenience function that works with source code strings.
    
    :param code: The Python source code to obfuscate
    :param seed: Optional random seed for reproducibility
    :param safe_mode: If True, skip star imports for safety
    :return: The obfuscated source code
    """
    if seed is not None:
        random.seed(seed)
    
    # Parse the code into an AST module
    tree = ast.parse(code)
    
    # Apply the obfuscation
    obfuscated_tree = stein_best(tree, seed=seed, safe_mode=safe_mode)
    
    # Convert back to source code
    try:
        # Try using ast.unparse (Python 3.9+)
        return ast.unparse(obfuscated_tree)
    except AttributeError:
        # Fallback to astor if available
        try:
            import astor
            return astor.to_source(obfuscated_tree)
        except ImportError:
            # Last resort: use the module printer from this package
            from pyobfstrsopsk import unparse
            return unparse(obfuscated_tree)
