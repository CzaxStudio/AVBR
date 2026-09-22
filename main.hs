import System.IO (hFlush, stdout)

-- | Core function that evaluates a simple algebraic string split into tokens.
-- It maps string operators to Haskell functions using pattern matching.
calculate :: [String] -> Maybe Double
calculate [leftStr, op, rightStr] =
    let left  = read leftStr :: Double
        right = read rightStr :: Double
    in case op of
        "+" -> Just (left + right)
        "-" -> Just (left - right)
        "*" -> Just (left * right)
        "/" -> if right == 0 
               then Nothing -- Prevent division by zero
               else Just (left / right)
        "^" -> Just (left ** right)
        _   -> Nothing -- Invalid operator
calculate _ = Nothing -- Invalid syntax (e.g., too many or too few arguments)

-- | Interactive REPL (Read-Eval-Print Loop)
main :: IO ()
main = do
    putStr "calc> "
    hFlush stdout -- Ensure prompt renders immediately
    input <- getLine
    
    if input == "quit" || input == "exit"
        then putStrLn "Goodbye!"
        else do
            -- Split input into tokens by whitespace (e.g., "5 + 3" -> ["5", "+", "3"])
            let tokens = words input
            case calculate tokens of
                Just result -> print result
                Nothing     -> putStrLn "Error: Invalid expression or division by zero."
            main -- Loop back to take the next input
