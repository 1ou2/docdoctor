source .env
# text retrieval by text ID
#curl $BACK/v1.0/text/12 -H "Authorization: Bearer $SECURED_TOKEN" -H "Content-Type: application/json"

# get similar text
# 
question="quels sont les objectifs du MLops?"
max_res=3
# "question":"'"$question"'" -> we want to expand shell variable 
# it is equivalent to "question" : "$question" but this syntax is incorret because of the enclosing '{ ... }'
#
#curl $BACK/v1.0/text/similar -H "Authorization: Bearer $SECURED_TOKEN" -H "Content-Type: application/json" \
#-d '{"question":"'"$question"'","max_result": '"$max_res"'}'

curl $BACK/v1.0/text/ask -H "Authorization: Bearer $SECURED_TOKEN" -H "Content-Type: application/json" \
-d '{"question":"'"$question"'","max_result": '"$max_res"'}'