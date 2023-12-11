import sys

n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
s = f"""*SUPPORT*
IN: 1 OUT: 1
IN: 3 OUT: 3
IN: 2 OUT: 2
IN: DAX OUT: DAX
IN: 2 after 3 OUT: 3 2
IN: 1 after 2 OUT: 2 1
IN: 2 thrice OUT:{' 2'*n}
IN: 2 surround 3 OUT: 2 3 2
IN: 1 thrice OUT:{' 1'*n}
IN: 3 surround 1 OUT: 3 1 3
IN: 2 thrice after 3 OUT: 3{' 2'*n}
IN: 3 after 1 surround 2 OUT: 1 2 1 3
IN: 2 after 3 thrice OUT:{' 3'*n} 2
IN: 3 surround 1 after 2 OUT: 2 3 1 3

*QUERY*
IN: DAX thrice OUT:{' DAX'*n}
IN: DAX thrice after 2 OUT: 2{' DAX'*n}
IN: 3 after DAX thrice OUT: {'DAX '*n}3
IN: DAX surround DAX after DAX thrice OUT: DAX DAX DAX{' DAX'*n}
IN: DAX surround 3 after 1 thrice OUT:{' 1'*n} DAX 3 DAX

*GRAMMAR*
1 -> 1
3 -> 3
2 -> 2
DAX -> DAX
u1 thrice ->{' [u1]'*n}
u1 surround u2 -> [u1] [u2] [u1]
x1 after x2 -> [x2] [x1]
u1 x1 -> [u1] [x1]"""
with open(
    "data_human/few_shot/val_gold/mini_scan.txt",
    "w",
) as f:
    f.write(s)
