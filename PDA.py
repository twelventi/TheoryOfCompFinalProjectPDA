#[print(str('a'*i + 'b'*i), all([x == 'a' for x in str('a'*i + 'b'*i)[:len(str('a'*i + 'b'*i))//2]]) and all([x == 'b' for x in str('a'*i + 'b'*i)[len(str('a'*i + 'b'*i))//2:]])) for i in range(1,11)]
import pprint

### 
#   
#   Theory of Computation
#   DPA to Recognize the Language L(G) = {a^nb^n | N >= 0}
#   
#   The Deterministic Pushdown Automata is defined as follows:
#   M = (
#     {p, q, qa, qb, q$}, 
#     {a, b, $}, 
#     {a, b, S}, 
#     Δ, 
#     p,
#    {q$}
#   )
#
#    Δ = {
#       (p, e, e)  -> (q, S)
#       (q, a, e)  -> (qa, e)
#       (qa, e, a) -> (q, e)
#       (q, b, e)  -> (qb, e)
#       (qb, e, b) -> (q, e)
#       (q, $, e)  -> (q$, e)
#       (qa, e, S) -> (qa, aSb)
#       (qb, e, S) -> (qb, e)
#   }
#
#   The grammar rules from which these are derived are:
#   R = {
#       S -> aSb
#       S -> e
#   }

def PDA(input_str):
    ### These are the rules for transition functions
    ### for the pushdown automata. It is represented 
    ### in python as a dictionary
    ### where key = the input (state, input symbol, stack symbol)
    ###       value = the transition (new state, chars to be pushed
    #                 to stack, rule number) (the rule number is for 
    #                 aesthetic table output)
    
    ### A dictionary is chosen here, because each state of the machine 
    #   only has one transition function, so we can read the machine 
    #   state, generate the key, and then access it by passing that 
    #   key to the dictionary
    rules = {
        ('p', 'e', 'e') : ('q', 'S', 0),
        ('q', 'a', 'e'): ('qa', 'e', 1),
        ('qa', 'e', 'a'): ('q', 'e', 2),
        ('q', 'b', 'e'): ('qb', 'e', 3),
        ('qb', 'e', 'b'): ('q', 'e', 4),
        ('q', '$', 'e') : ('q$', 'e', 5),
        ('qa', 'e', 'S'):('qa', 'aSb', 6),
        ('qb', 'e', 'S'):('qb', 'e', 7)    
    }                                       
    
    ### This dictionary stores the current state of the machine
    ### state is the state of the machine
    ### unread_input is the list of unread characters
    ### stack is the items on the stack
    ### rule is the rule used to get to this state
    table = {
        "state": 'p',
        "unread_input" : input_str,
        "stack" : [],
        "rule" : "-"
    }

    ### This will store the number of steps taken before we reach a conclusion
    count = 0

    ### Function to output one table row
    def format_t(tbl, ct, rule):
        state = tbl["state"],
        unr_i = tbl["unread_input"],
        stack = tbl["stack"],
        rulen = tbl["rule"],

        print(f'{str(count).center(5)}|{str(state[0]).center(5)}|{str(unr_i[0]).center(30)}|{("".join(stack[0])).center(15)}|{str(rule).center(3)} | {"S -> e" if rule == 8 else ("S -> aSb" if rule ==7 else " ")}')

    ### Output the table header
    print('count|state|         unread input         |     stack     |rule')

    ### Caclulate the DPA
    ### Repeat while there are still items on the stack, or unread inputs
    while table["state"] != 'q$' or len(table["unread_input"]) > 0 or len(table["stack"]) > 0:

        ### Initialize variables for easier code readability
        state = table["state"]
        input_sym = 'e' if len(table["unread_input"]) == 0 else table["unread_input"][0]
        stack = table["stack"]

        ### Output the current state of the machine
        format_t(table, count, table["rule"])

        ### Figure out what the key will be for the transition function
        #   first we try to create a key that is
        #   (state, input symbol, stack symbol)
        key = (state, input_sym, 'e' if len(stack) == 0 else stack[0])

        ### If there's no rule associated with this key,
        #   try a key that is:
        #   (state, empty, stack symbol)
        #   We are not required to read an input symbol
        #   during every transition
        if key not in rules.keys():
            key = (state, 'e', 'e' if len(stack) == 0 else stack[0])
        
        ### If there's no key that is associated with the stack symbol
        #   Attempt it without reading a stack symbol, but also reading
        #   the input symbol
        if key not in rules.keys():
            key = (state, input_sym, 'e')

        ### If all the possible keys that match this machine state
        #   do not exist in the rules, then the input string does 
        #   not match the grammar and we can return false, because
        #   the input string will not be validated
        if key not in rules:
            return False

        ### At this point, whatever the value of key is, there will be a 
        #   corresponding rule, so set the new state to the state defined
        #   by the transition function
        ### Also, update the unread input. If the transition function has 
        #   us read an input, then remove it from the unread input, otherwise
        #   keep it the same
        table["state"] = rules[key][0]
        table["unread_input"] = table["unread_input"][1:] if key[1] != 'e' else table["unread_input"]

        ### Pop an item off of the stack if the key "consumed"
        #   the stack item
        if len(stack) > 0:
            if key[2] == stack[0]:
                stack.pop(0)

        ### Push the new items on to the stack
        #   rules[key][1][::-1] loops through the
        #   pending items to be pushed in reverse order

        ##  The reason this is done is because if your stack, for example
        #   looks like this: aabbb, and you need to push AB onto the stack
        #   the resulting stack will look like this: ABaabbb, not BAaabbb
        #   so we have to push the multiple items from right to left
        for ch in rules[key][1][::-1]:
            if(ch != 'e'):
                stack.insert(0, ch)


        # update the rule that got the machine to this state
        table["rule"] = rules[key][2]

        # increase the count
        count += 1

    ### At this point, the loop ended because there is nothing left to
    #   read from the input string, but we still need to output the last
    #   row of the table
    format_t(table, count, table["rule"])
    
    ### If there are still items in the stack, then the input string is
    #   invalid, so this will return false, otherwise, it returns true
    return True

### Python semantics to run this only if this file was directly run
#   to run custom strings through the code, this file can be run with python -i
#   and then running the function PDA(<input string>)
if __name__ == "__main__":
    results = []

    # generates the 10 input strings to be used as a test
    for i in range(1,11):
        string = 'a'*i + 'b'*i +'$'
        result = (string, PDA(string))
        print(string, result[1])
        results.append(result)
        print()

    ### invalid strings to test as well
    test_invalid_strings = [
        "aabbbbb$",
        "bbbbb$",
        "aaaaaab$",
        "ababab$",
        "aaaaa$",
    ]

    #run the PDA on invalid strings
    for string in test_invalid_strings:
        result = (string, PDA(string))
        print(string, result[1])
        results.append(result)
        print()

    ### output the results
    pprint.pprint(results)