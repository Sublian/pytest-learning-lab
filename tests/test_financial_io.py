# tests/test_financial_io.py
import csv
from calculator.financial import FinancialCalculator

def test_compound_from_csv(tmp_path):
    file = tmp_path / "data.csv"
    rows = [
        ("principal","rate","time"),
        ("1000","0.05","2"),
        ("500","0.1","1"),
    ]
    with open(file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    results = []
    with open(file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = float(row["principal"])
            r = float(row["rate"])
            t = int(row["time"])
            results.append(round(FinancialCalculator.compound_interest(p, r, t), 2))

    assert results == [1102.5, 550.0]  # 1000*(1+0.05)^2 = 1102.5 ; 500*(1+0.1)^1 = 550
