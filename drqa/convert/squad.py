import json
import csv
import argparse


def convert_csv_to_json_format(files, output_file):
    data = []
    id = 0
    paragraph = "skaljfkldhjkcdhdnjkn"
    cnt = 0
    all = 0
    for FILE in files:
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
    with open(output_file, "w") as ftw:
        json.dump(dict(data=data, version=1.1), ftw, ensure_ascii=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_squad', type=str, help='Path to dataset, translated squad')
    parser.add_argument('file_sber', type=str, help='Path to dataset, sberbank qa dataset')
    parser.add_argument('out_file', type=str, help='Path to output file')
    args = parser.parse_args()
    convert_csv_to_json_format([args.file_squad, args.file_sber], args.outfile)
