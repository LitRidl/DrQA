import json
import csv


FILE = 'train_task_b.csv'

data = []
id = 144512211264
paragraph = "skaljfkldhjkcdhdnjkn"
cnt = 0
all = 0
try:
    with open(FILE, 'r') as ftr:
        reader = csv.DictReader(ftr)
        for row in reader:
            if row["paragraph"] != paragraph:
                id += 1
                paragraph = row["paragraph"]
                data.append(dict(title='doc_{}'.format(id), paragraphs=[dict(context=paragraph, qas=[])]))
            qas = data[-1]["paragraphs"][0]["qas"]
            index = paragraph.find(row["answer"])
            all += 1
            if index == -1:
                continue
            cnt += 1
            qas.append(dict(question=row["question"], id=cnt+10**5, answers=[dict(text=row["answer"],
                                                                            answer_start=index)]))
except Exception as e:
    print(cnt)

print(cnt, cnt / all)
with open("sber_output.json", "w") as ftw:
    json.dump(dict(data=data, version=1.1), ftw, ensure_ascii=False)

