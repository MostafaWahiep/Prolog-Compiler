
def Match(a,j, Tokens):
    output=dict()
    if(j<len(Tokens)):
        Temp=Tokens[j].to_dict()
        if(Temp['token_type']==a):
            j+=1
            output["node"]=[Temp['Lex']]
            output["index"]=j
            return output
        else:
            output["node"]=["error"]
            output["index"]=j+1
            errors.append("Syntax error : "+Temp['Lex']+" Expected dot")
            return output
    else:
        output["node"]=["error"]
        output["index"]=j+1
        return output