import lib_10kq_seg_v1 as lib10kq


infile = "../segout01/urlfile_clean02.htm.txt"
outfile = "../segout01/test_output03.txt"
with open(infile, "r") as fh:
    clean_text = fh.read()

pure_text2 = lib10kq.pretty_text(clean_text)

# print(pure_text2)
with open(outfile, "w") as fh:
    fh.write(pure_text2)

