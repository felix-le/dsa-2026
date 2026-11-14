"""
{
openThese = ["(", "{", "["]
closeThese = [")","}","]"]

if s.length === 0 return false
!s.include("}") && !s.include("]")&& !s.include(")") return false
  orderOpenParentheses= []

for (let i = 0; i < s.length; i ++){

  if openThese.include(s[i]){
    orderOpenParentheses.push(s[i])
  };

  # compare with the close parentheses:

  if closeThese.include(s[i]){
    orderOpenParentheses.length === 0 return false
    compareFn(orderOpenParentheses[orderOpenParentheses.length-1], s[i]) ? orderOpenParentheses.pop() : return false
  }

}
  return orderOpenParentheses.length === 0
}
const compareFn = (o:string, c:string): Boolean{
  o === "(" && c === ")" return true
  o === "[" && c === "]" return true
  o === "{" && c === "}" return true
  return false
}
"""
def isValid(s):
  open_these = ["{", "[", "("]
  close_these = ["}," "]" ,")"]

  stack = []
  for ch in s:
    if ch in open_these:
      stack.append(ch)
    if ch in close_these:
      if len(stack)==0:
        return False
      if not compare_fn(stack[-1], ch):
        return False
      stack.pop()
  return len(stack) == 0

def compare_fn(o,c):
  if o == "(" and c==")":
    return True
  if o == "{" and c == "}":
    return True
  if o == "[" and c == "]":
    return True
  return False
