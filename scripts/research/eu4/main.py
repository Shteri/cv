import gen, opel, renault, copies, fiat
opel.main(); renault.main(); copies.main(); fiat.main()
gen.save_rules()
print(len(gen.WRITTEN), 'files', len(gen.RULES), 'rules')
