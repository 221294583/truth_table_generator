import pro


test=pro.pro('not ((p and not q)then(p or q))')
test.table_base()
test.bracket()
print(test.brackets)
test.iterate()
test.print()