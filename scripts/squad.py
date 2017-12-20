import json
import csv


FILE = 'SQuAD_ru.csv'

data = []
id = 0
paragraph = "skaljfkldhjkcdhdnjkn"
cnt = 0
all = 0
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
        qas.append(dict(question=row["question"], id=cnt, answers=[dict(answer=row["answer"],
                                                                        answer_start=index)]))
print(cnt, cnt / all)
with open("sqad_output.json", "w") as ftw:
    json.dump(dict(data=data, version=1.1), ftw, ensure_ascii=False)

