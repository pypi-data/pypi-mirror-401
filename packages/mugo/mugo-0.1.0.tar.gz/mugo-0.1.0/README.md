
# combinatory optimization for choosing top-K SNPs to max gene expression for Borzoi

## project overview
Borzoi using gencode v41, use this which follow hg38, Geuvadis using hg19, should trans those VCF from hg19 to hg38 first. 

link to netlify docsite: 



## plan 
1. check those SNPs whether overlap with some motifs and appeared in pair in GTEx dataset, or motif analysis, or compare with MPRA (Massively Parallel Reporter Assays), if can match it can make a good journal, if not can target at KDD, and if not found Epistasis, target at dataset track of NIPS show borzoi can not capture Epistasis. 



## dataset
using Geuvadis dataset, which have vcf files and can points out position for about 800 SNPs for each gene, and then do training. 

## TODO list
1. extend to enformer 
2. extend to other two tracks, and also check for disease enrichment whether diseases related to correspond tissue can have higher score. 
总的架构enformer一个scirpt，borzoi一个script，但是不同的tissue要在代码内部直接加args实现比如--tissue，--index这种防止项目过于杂乱。

