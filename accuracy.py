import csv

with open("results/mm_results.csv") as file:
    data = file.read()
    winners = data.split(",")

with open("results/accuracy.csv", 'w', newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "RO64", "RO32", "S16", "E8", "F4", "NCG", "Total"])

with open("results/results1.csv", 'r') as csv_file:
    reader = csv.reader(csv_file)
    for bid, bracket in enumerate(reader):
        bin_ctr = [0 for i in range(63)]
        for game in range(63):
            if winners[game] == bracket[game]:
                bin_ctr[game] = 1
        ro64 = sum(bin_ctr[0:32]) * 10
        ro32 = sum(bin_ctr[32:48]) * 20
        s16 = sum(bin_ctr[48:56]) * 40
        e8 = sum(bin_ctr[56:60]) * 80
        f4 = sum(bin_ctr[60:62]) * 160
        ncg = bin_ctr[62] * 320
        total = ro64 + ro32 + s16 + e8 + f4 + ncg
        bracket_data = [bid, ro64, ro32, s16, e8, f4, ncg, total]
        with open("results/accuracy.csv", 'a', newline="") as accuracy:
            writer = csv.writer(accuracy)
            writer.writerow(bracket_data)
        print(bid)