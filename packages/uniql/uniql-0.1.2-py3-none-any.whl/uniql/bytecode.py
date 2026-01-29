from enum import Enum, auto

#定義一組「虛擬機能懂的指令」
class OpCode(Enum): # 機器指令集（Instruction Set）
    LOAD_FIELD = auto()    # 讀欄位
    LOAD_CONST = auto()    # 常數
    
    # 數學運算
    EQ = auto()   # ==
    NE = auto()   # !=
    GT = auto()   # >
    LT = auto()   # <
    GE = auto()   # >=
    LE = auto()   # <=

    # 函數指令
    YEAR = auto()
    MONTH = auto()
    DATE = auto()
    UPPER = auto()
    LOWER = auto()
    CONCAT = auto()
    ROUND = auto()
    CEIL = auto()
    FLOOR = auto()

    # 比較運算
    IN = auto()        
    NOT_IN = auto()    
    LIKE = auto()      

    # 邏輯運算
    AND = auto()
    OR = auto()
    NOT = auto()

    # 「程式跑完了，把 stack 最上面的結果當成答案」
    RETURN = auto()
