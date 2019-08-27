# coding: utf8

import sys
import os

outname = 'summary'


class Transaction:
    def __init__(self, line):
        l = [i.strip() for i in line.split(',')]
        self.flow_sn = l[0]
        self.biz_sn = l[1]
        self.order_sn = l[2]
        self.product = l[3]
        self.time = l[4]
        self.account = l[5]
        self.income_account = float(l[6])
        self.expenditure = float(l[7])
        self.balance = float(l[8])
        self.sale_channel = l[9]
        self.biz_kind = l[10]
        self.remark = l[11]
        l = self.remark.split('=')
        self.project = l[0] if len(l) > 0 else ""
        self.person = l[2] if len(l) == 3 else ""

    def __str__(self):
        line = ''
        for k, v in self.__dict__.items():
            line += '%s=%s,' % (k, v)
        return line[:-1]


class PeriodStat:
    def __init__(self, period, project):
        self.period = period
        self.project = project
        self.persons = set()
        self.transaction_count = 0
        self.sum_amount = 0.

    def __str__(self):
        return '%s\tpersons=%d, transcations=%d, amount=%f' % (
            self.period, len(self.persons), self.transaction_count, self.sum_amount)


class PersonDonation:
    def __init__(self, name, month):
        self.name = name
        self.month = month
        self.transaction_count = 0
        self.donation = 0.

    def __str__(self):
        return '%s\ttranscations=%d, amount=%f' % (
            self.name, self.transaction_count, self.donation)


def read_details(csvfile):
    print('* reading %s' % csvfile)
    transactions = []
    sepline = False
    begline = False
    for line in file(csvfile):
        if not sepline:
            if '#----------' in line:
                sepline = True
            continue
        elif not begline:
            begline = True
            continue
        else:
            if '#----------' in line:
                # ending
                break
            o = Transaction(line)
            transactions.append(o)
    return transactions


indir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

subdirs = os.listdir(indir)
subdirs = [d for d in subdirs if d.find("_") == 8]
subdirs.sort()

transactions = []
for sub in subdirs:
    if sub == outname:
        continue
    sub = os.path.join(indir, sub)
    if not os.path.isdir(sub):
        continue
    for f in os.listdir(sub):
        if not f.endswith('.csv'):
            continue
        if '(' in f and ')' in f:
            continue
        csvfile = os.path.join(sub, f)
        transactions.extend(read_details(csvfile))

months = dict()
dates = dict()
persons = dict()

for t in transactions:
    m = t.time[:7]
    p = t.project
    k = '%s-%s' % (m, p)
    if k not in months:
        months[k] = PeriodStat(m, p)
    m_stat = months[k]
    d = t.time[:10]
    k = '%s-%s' % (d, p)
    if k not in dates:
        dates[k] = PeriodStat(d, p)
    d_stat = dates[k]
    p = t.person
    k = '%s-%s' % (p, m)
    if k not in persons:
        persons[k] = PersonDonation(p, m)
    p_stat = persons[k]

    # person
    m_stat.persons.add(p)
    d_stat.persons.add(p)
    # transaction
    m_stat.transaction_count += 1
    m_stat.sum_amount += t.income_account
    d_stat.transaction_count += 1
    d_stat.sum_amount += t.income_account
    p_stat.transaction_count += 1
    p_stat.donation += t.income_account

print("> output: ")
outdir = os.path.join(indir, outname)
if not os.path.exists(outdir):
    os.makedirs(outdir)

outf = os.path.join(outdir, 'months.csv')
print("* write to %s" % outf)
with file(outf, mode='w') as writer:
    writer.write("month,project,persons,transactions,amount\n")
    keys = list(months.keys())
    keys.sort()
    for k in keys:
        m = months[k]
        writer.write("%s,%s,%d,%d,%.3f\n" % (m.period, m.project, len(m.persons), m.transaction_count, m.sum_amount))

outf = os.path.join(outdir, 'dates.csv')
print("* write to %s" % outf)
with file(outf, mode='w') as writer:
    writer.write("date,project,persons,transactions,amount\n")
    keys = list(dates.keys())
    keys.sort()
    for k in keys:
        d = dates[k]
        writer.write("%s,%s,%d,%d,%.3f\n" % (d.period, d.project, len(d.persons), d.transaction_count, d.sum_amount))

outf = os.path.join(outdir, 'persons.csv')
print("* write to %s" % outf)
with file(outf, mode='w') as writer:
    writer.write("person,month,transactions,amount\n")
    keys = list(persons.keys())
    keys.sort()
    for k in keys:
        p = persons[k]
        writer.write("%s,%s,%d,%.3f\n" % (p.name, p.month, p.transaction_count, p.donation))
