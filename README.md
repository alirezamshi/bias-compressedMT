What Do Compressed Multilingual Machine Translation Models Forget?
=================

<p align="center">
  <img src="logo.png" width="700"/>
</p>

We assess the impact of compression methods on Multilingual Neural Machine Translation models (MNMT) for various language groups, gender, and semantic biases by extensive analysis of compressed models on different machine translation benchmarks, i.e. FLORES-101, MT-Gender, and DiBiMT. We show that the performance of under-represented languages drops significantly, while the average BLEU metric only slightly decreases. Interestingly, the removal of noisy memorization with compression leads to a significant improvement for some medium-resource languages. Finally, we demonstrate that compression amplifies intrinsic gender and semantic biases, even in high-resource languages.

Contents
---------------
- [spBLEU-based Analysis](#spbleu)
- [CHRF-based Analysis](#chrf)
- [Bias Analysis](#bias)
- [Citation](#citation)

<a name="spbleu"/>  

spBLEU-based Analysis
-------------

The ```Analysis_BLEU``` class requires a metadata data in the following format:

```
[{'pairs': ## list of pairs for be evaluated (format source_id-target_id),
'types': ## type of language pair in the benchmark 
'convert_type': ## definition of different language types in "types" column,
'bitext': ## amount of training data for languages in the benchmark]
```
Sample ```metadata.json``` is provided.

```Analysis_BLEU``` class can be used as:

```
from bleu import Analysis_BLEU
analysis = Analysis_BLEU('metadata.json')
analysis.read_files('sample/base_flores101.txt','sample/model_flores101.txt')

## relative score based on type of 1)language pair 2) target 3) source
analysis.diff_bucket_type()
## relative score vs. amount of bitext data for different language pairs
analysis.scatter_plot_diff()
```

<a name="chrf"/>  

CHRF-based Analysis
-------------

We use sentence-level CHRF from [sacrebleu]('https://github.com/mjpost/sacrebleu') repository. It can be used as:

```
import sacrebleu
generated = "Co nás nejvíc trápí, protože lékaři si vybírají, kdo bude žít a kdo zemře."
reference = "Nejvíce smutní jsme z toho, že musíme rozhodovat o tom, kdo bude žít a kdo zemře."
sacrebleu.sentence_chrf(generated, [reference], 6, 3)
```


<a name="bias"/>  

Bias Analysis
-------------

We use [MT-Gender](https://github.com/gabrielStanovsky/mt_gender) and [DiBiMT](https://nlp.uniroma1.it/dibimt/) benchmarks to evaluate gender and semantic biases, respectively. 

<a name="citation"/>  

Citation
-------------

If you use this code for your research, please cite the following work:
```
@inproceedings{mohammadshahi-etal-2022-compressed,
    title = "What Do Compressed Multilingual Machine Translation Models Forget?",
    author = "Mohammadshahi, Alireza  and
      Nikoulina, Vassilina  and
      Berard, Alexandre  and
      Brun, Caroline  and
      Henderson, James  and
      Besacier, Laurent",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2022",
    month = dec,
    year = "2022",
    address = "Abu Dhabi, United Arab Emirates",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.findings-emnlp.317",
    pages = "4308--4329",
    abstract = "Recently, very large pre-trained models achieve state-of-the-art results in various natural language processing (NLP) tasks, but their size makes it more challenging to apply them in resource-constrained environments. Compression techniques allow to drastically reduce the size of the models and therefore their inference time with negligible impact on top-tier metrics. However, the general performance averaged across multiple tasks and/or languages may hide a drastic performance drop on under-represented features, which could result in the amplification of biases encoded by the models. In this work, we assess the impact of compression methods on Multilingual Neural Machine Translation models (MNMT) for various language groups, gender, and semantic biases by extensive analysis of compressed models on different machine translation benchmarks, i.e. FLORES-101, MT-Gender, and DiBiMT. We show that the performance of under-represented languages drops significantly, while the average BLEU metric only slightly decreases. Interestingly, the removal of noisy memorization with compression leads to a significant improvement for some medium-resource languages. Finally, we demonstrate that compression amplifies intrinsic gender and semantic biases, even in high-resource languages.",
}
```
Have a question not listed here? Open [a GitHub Issue](https://github.com/alirezamshi/bias-compressedMT/issues) or 
send us an [email](alireza.mohammadshahi@idiap.ch).
