# 1. Introduction

Large language models (LLMs) have been advancing rapidly since the introduction of the transformer architecture [^Vaswani2017]; however, they remain costly to train and deploy because they contain billions to trillions of parameters as general-purpose sequence models [^Cottier2024]. To address this challenge, we develop a small language model (SLM) with a fine-tuning feature that is customized for healthcare applications, demonstrating the SLM's cost and time efficiency when applied to a specific task within a defined domain. We design our SLM by combining the strengths of Doc2Vec and bidirectional encoder representations from transformers (BERT) to examine how online reviews reflect physicians' service quality, and how this, in turn, influences the demand for online consultations. The algorithm is designed to extract service quality scores from online physician reviews using a health service quality framework established by health authorities to evaluate healthcare provider performance [^AHRQ2019], which avoids random text mining based on probabilistic methods without a theory supporting guideline as previous studies have done [^Wan2021] [^Xu2021]. We then analyze how these quality scores affect patients' decisions to make appointments for online consultation.

We choose online consultation as our study instance because it is in one of the highest demands among all healthcare services. Online consultation allows physicians to deliver healthcare service through electronic channels [^Dorsey2016]. This service has experienced an astonishing 154% surge in April 2020 compared with previous year [^Koonin2020]. The global telehealth market is projected to experience substantial growth, with a compound annual growth rate of 15.8% [^GrandViewResearch2024].

However, patients often face information asymmetry, making it challenging to assess the quality of a physician's service when deciding for online consultation. Online physician reviews have gained prominence for patients to share their personal experiences since the advent of Web 2.0, which can reduce the information asymmetry, and have been prevalent in many countries [^Gao2012] [^Emmert2013] [^Hao2015]. With the rapid advancements in natural language processing (NLP) technology, researchers have begun to utilize physician reviews to gain rich and previously inaccessible insights into patient experiences [^Hao2017] and to examine how patients perceive healthcare service quality based on online ratings [^Jiang2024]. Research has found that physician reviews can effectively assess a physician's service quality [^Gao2015], can impact patients' choices of primary care providers [^Yaraghi2018] and can influence offline consultation demand [^Xu2021] or online consultation demand [^Wan2021]. However, existing research lacks a systematic approach to utilize the latest NLP technology within theory-supported healthcare service quality evaluation frameworks to extract meaningful healthcare service quality assessments from online reviews and examine the service quality's impact on online consultations. First, prior studies rely on aspect-based sentiment analysis (ABSA) methods that mine service reviews without applying a theoretical or clinically grounded framework [^Wan2021] [^Xu2021]. As a result, they fail to capture the clinically validated dimensions of healthcare quality that regulatory authorities and medical professionals consider essential for healthcare effectiveness. Second, prior studies' sentiment analysis has not leveraged the latest NLP technologies tailored specifically for healthcare contexts [^Wan2021] [^Xu2021]. To overcome these challenges, we adopt the widely used health service quality evaluation framework, SEPTED, developed by the Agency for Healthcare Research and Quality (AHRQ) [^AHRQ2019], and refine it into the SEPTE model to extract and evaluate healthcare providers' service quality from online reviews.

Our study makes several contributions. Methodologically, we develop an SLM (Doc-BERT) tailored to the healthcare context and demonstrate that a task-aligned, domain-tuned SLM can outperform a wide range of existing NLP approaches, including recent general LLMs, for multidimensional sentiment analysis of physician reviews. This performance advantage reflects that SLM has the advantage of full domain adaptation and computational cost compared with LLMs in this context. Theoretically, we adopt and refine a quality evaluation framework for healthcare service at the provider level, ensuring that our SLM purposefully analyzes online reviews with a focus on providers' service quality rather than random text mining. To the best of our knowledge, the present study is among the first in the information systems field to employ this framework. Empirically, our findings demonstrate that physician reviews have a significant impact on the demand for online consultation, which offers practical implications for online healthcare providers and healthcare organizations seeking to enhance service quality and, consequently, increase online consultation demand.

---

## References (Cited in Introduction)

[^Vaswani2017]: Vaswani A, Shazeer N, Parmar N, et al. (2017) Attention is all you need. *Proc. 31st Internat. Conf. Neural Inform. Processing Systems*, 5998–6008.

[^Cottier2024]: Cottier B, Rahman R, Fattorini L, et al. (2024) The rising costs of training frontier AI models. *Preprint*, arXiv:2405.21015.

[^AHRQ2019]: AHRQ (2019) Examples of physician quality measures for consumers. Retrieved December 22, https://www.ahrq.gov/talkingquality/measures/setting/physician/examples.html.

[^Wan2021]: Wan Y, Peng Z, Wang Y, et al. (2021) Influencing factors and mechanism of doctor consultation volume on online medical consultation platforms based on physician review analysis. *Internet Res.* 31(6):2055–2075.

[^Xu2021]: Xu Y, Armony M, Ghose A (2021) The interplay between online reviews and physician demand: An empirical investigation. *Management Sci.* 67(12):7344–7361.

[^Dorsey2016]: Dorsey ER, Topol EJ (2016) State of telehealth. *New England J. Medicine* 375(2):154–161.

[^Koonin2020]: Koonin LM, Hoots B, Tsang CA, et al. (2020) Trends in the use of telehealth during the emergence of the Covid-19 pandemic—United States, January–March 2020. *Morbidity and Mortality Weekly Rep.* 69(43):1595–1599.

[^GrandViewResearch2024]: Grand View Research (2024) Healthcare IT market size, share & trends analysis report. Retrieved October 25, https://www.grandviewresearch.com/industry-analysis/healthcare-it-market.

[^Gao2012]: Gao GG, McCullough JS, Agarwal R, Jha AK (2012) A changing landscape of physician quality reporting: Analysis of patients' online ratings of their physicians over a 5-year period. *J. Medical Internet Res.* 14(1):e38.

[^Emmert2013]: Emmert M, Meier F (2013) An analysis of online evaluations on a physician rating website: Evidence from a German public reporting instrument. *J. Medical Internet Res.* 15(8):e2655.

[^Hao2015]: Hao H (2015) The development of online doctor reviews in China: An analysis of the largest online doctor review website in China. *J. Medical Internet Res.* 17(6):e134.

[^Hao2017]: Hao H, Zhang K, Wang W, Gao G (2017) A tale of two countries: International comparison of online doctor reviews between China and the United States. *Internat. J. Medical Inform.* 99:37–44.

[^Jiang2024]: Jiang L, Hou J, Ma X, Pavlou PA (2024) Punished for success? A natural experiment of displaying clinical hospital quality on review platforms. *Inform. Systems Res.* 36(1):285–306.

[^Gao2015]: Gao G, Greenwood BN, Agarwal R, McCullough J (2015) Vocal minority and silent majority: How do online ratings reflect population perceptions of quality? *MIS Quart.* 39(3):565–589.

[^Yaraghi2018]: Yaraghi N, Wang W, Gao G, Agarwal R (2018) How online quality ratings influence patients' choice of medical providers: Controlled experimental survey study. *J. Medical Internet Res.* 20(3):e99.

[^Singh2017]: Singh A, Alryalat MAA, Alzubi JA, Sarma HK (2017) Understanding Jordanian consumers' online purchase intentions: Integrating trust to the Utaut2 framework. *Internat. J. Appl. Engrg. Res.* 12(20):10258–10268.

[^Guo2020]: Guo J, Wang X, Wu Y (2020) Positive emotion bias: Role of emotional content from online customer reviews in purchase decisions. *J. Retailing Consumer Services* 52:101891.
