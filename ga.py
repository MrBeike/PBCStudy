#TODO 一站到底
import json
results = []
floor_info_json = None
floor_info_dict = json.loads(floor_info_json) 
correctValue = floor_info_dict['correctValue']
radixValue = floor_info_dict['radixVlue']
allCorrectValue = floor_info_dict['allCorrectValue']

# 问题的type是否会影响答案？ 2为判断，0为单选
for index,item in enumerate(floor_info_dict['questions']):
    questionId = item['id']
    for choice in item['items']:
        if choice['isAnswer'] == 1:
            result = choice['id']
    resultValue = correctValue + (index * radixValue) + (100 if index == len(floor_info_dict['questions']) else 0)

answer = {
    "questionId":questionId,
    "result":result,
    "resultValue":resultValue,
    "isTrue":1
}

results.append(answer)
ga_answeers = {
    "floor":floor,
    "floorValue":floorValue,
    "floorPassed":1,
    "results":results
}