
#Analayzing the data
def analayze_data(data: object) ->str:
    match data:
     case int() | float() as num if num>0:
      return f"You have entered an postive number {num}"
     case str() as text if text.strip():
       return f"Your messgae is {text}"
     case tuple() | list() as seq if seq:
       return f"Your seq length is {len(seq)}"
     case dict() as d if d :
    #    return f"Key value pairs of the dict is {key}"
         return f"Dictionary with key pairs is {' , '.join(d.keys())}"
     case _:
      return "UnHandled datatype or Empty Value."
    


#Example usage 
# data=analayze_data(2)
# print(data)
# data= analayze_data("Gowri")
# print(data)

tuple_data=("Voonna","Gowri","Ganesh")
fruits_list=["Apple","Banna","Grap"]
dict_data={"Name":"Voonna", "Age":22}
# print(analayze_data(tuple_data))
# print(analayze_data(fruits_list))
# print(analayze_data(dict_data))   # It returns key names
# print(analayze_data(""))    #It returns an Unhandled datatype or Empty Value
#print(analayze_data(10_000_000))
#print(analayze_data({}))  

#Enhanced switch with pattern matching.

def process_event(event: dict) ->str:
    match event:
     case {'type': 'user', 'action' : 'logged_in', "id":id}:
       return f"User {id} logged_in"
     case {'type' : 'user','action' :'logged_out',"id":id}:
      return f"User {id} logged_out."
     case { 'type':'Error', 'Code':code,'msg':msg}:
      return f" Error {code} : {msg}"
     case {'type':'System_Error',**details}:   # ** means it take whether pattern matching or unmatching it will .
       return f"System event details : { details}"
     case _ :
       return "Unevent Exist"

user_loggedin = { 'type': 'user', 'action' : 'logged_in', "id":12}
print(process_event(user_loggedin))
user_error = {'type':'Error','Code':404,'msg':'Internal server Error'}
print(process_event(user_error))
system_error={'type':'System_Error','Version':'1_00_000','Error_code':404}
print(process_event(system_error))
print(process_event({}))
