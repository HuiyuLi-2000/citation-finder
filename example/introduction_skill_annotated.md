1. Introduction

Large language models (LLMs) have been advancing rapidly since the introduction of the transformer architecture [1,2,3]; however, they remain costly to train and deploy because they contain billions to trillions of parameters as general-purpose sequence models [4,5,1]. To address this challenge, we develop a small language model (SLM) with a fine-tuning feature that is customized for healthcare applications, demonstrating the SLM's cost and time efficiency when applied to a specific task within a defined domain. We design our SLM by combining the strengths of Doc2Vec and bidirectional encoder representations from transformers (BERT) [6,7,8] to examine how online reviews reflect physicians' service quality, and how this, in turn, influences the demand for online consultations. The algorithm is designed to extract service quality scores from online physician reviews using a health service quality framework established by health authorities to evaluate healthcare provider performance [9,10,11], which avoids random text mining based on probabilistic methods without a theory supporting guideline as previous studies have done [12,13,14]. We then analyze how these quality scores affect patients' decisions to make appointments for online consultation.

We choose online consultation as our study instance because it is in one of the highest demands among all healthcare services. Online consultation allows physicians to deliver healthcare service through electronic channels. This service has experienced an astonishing 154% surge in April 2020 compared with previous year [15,16,17]. The global telehealth market is projected to experience substantial growth [18,19,20], with a compound annual growth rate of 15.8% [21,19,22].

However, patients often face information asymmetry [23,24,25], making it challenging to assess the quality of a physician's service when deciding for online consultation. Online physician reviews have gained prominence for patients to share their personal experiences since the advent of Web 2.0 [26,27,28], which can reduce the information asymmetry, and have been prevalent in many countries. With the rapid advancements in natural language processing (NLP) technology, researchers have begun to utilize physician reviews to gain rich and previously inaccessible insights into patient experiences and to examine how patients perceive healthcare service quality based on online ratings [29,30,31]. Research has found that physician reviews can effectively assess a physician's service quality [32,33,34], can impact patients' choices of primary care providers and can influence offline consultation demand or online consultation demand [23,35,36]. However, existing research lacks a systematic approach to utilize the latest NLP technology within theory-supported healthcare service quality evaluation frameworks to extract meaningful healthcare service quality assessments from online reviews and examine the service quality's impact on online consultations. First, prior studies rely on aspect-based sentiment analysis (ABSA) methods that mine service reviews without applying a theoretical or clinically grounded framework [37,38,39]. As a result, they fail to capture the clinically validated dimensions of healthcare quality that regulatory authorities and medical professionals consider essential for healthcare effectiveness [40,10,41]. Second, prior studies' sentiment analysis has not leveraged the latest NLP technologies tailored specifically for healthcare contexts [42,43,44]. To overcome these challenges, we adopt the widely used health service quality evaluation framework, SEPTED [12,45,46], developed by the Agency for Healthcare Research and Quality (AHRQ) [47,48,49], and refine it into the SEPTE model to extract and evaluate healthcare providers' service quality from online reviews.

Our study makes several contributions. Methodologically, we develop an SLM (Doc-BERT) tailored to the healthcare context and demonstrate that a task-aligned, domain-tuned SLM can outperform a wide range of existing NLP approaches, including recent general LLMs [50,51,52], for multidimensional sentiment analysis of physician reviews. This performance advantage reflects that SLM has the advantage of full domain adaptation and computational cost compared with LLMs in this context. Theoretically, we adopt and refine a quality evaluation framework for healthcare service at the provider level, ensuring that our SLM purposefully analyzes online reviews with a focus on providers' service quality rather than random text mining. To the best of our knowledge, the present study is among the first in the information systems field to employ this framework. Empirically, our findings demonstrate that physician reviews have a significant impact on the demand for online consultation, which offers practical implications for online healthcare providers and healthcare organizations seeking to enhance service quality and, consequently, increase online consultation demand.

---

## References

[1] Zhao, W.X., Zhou, K., Li, J., et al. (2026). A Survey of Large Language Models. *Frontiers of Computer Science*. doi:10.1007/s11704-026-60308-3 【support=0.75 | tier=0.8 | composite=0.865】

[2] Zhao, H., Chen, H., Yang, F., et al. (2024). Explainability for Large Language Models: A Survey. *ACM Transactions on Intelligent Systems and Technology*. doi:10.1145/3639372 【support=0.70 | tier=0.95 | composite=0.895】

[3] Naveed, H., Khan, A.U., Qiu, S., et al. (2025). A comprehensive overview of large language models. *ACM Transactions on Intelligent Systems and Technology*. 【support=0.75 | tier=0.8 | composite=0.865】

[4] Subramanian, S. (2024). Large Language Model-based solutions: how to deliver value with cost-effective generative AI applications. 【support=0.85 | tier=0.8 | composite=0.895】

[5] Johnsen, M. (2024). Large language models (LLMs). 【support=0.85 | tier=0.8 | composite=0.895】

[6] Seilsepour, A., Ravanmehr, R., Nassiri, R. (2023). Topic sentiment analysis based on deep neural network using document embedding technique. *The Journal of Supercomputing*. 【support=0.90 | tier=0.6 | composite=0.770】

[7] Mutinda, J., Mwangi, W., Okeyo, G. (2023). Sentiment analysis of text reviews using lexicon-enhanced BERT embedding (LeBERT) model with convolutional neural network. *Applied Sciences*. 【support=0.70 | tier=0.8 | composite=0.770】

[8] Atandoh, P., Zhang, F., Adu-Gyamfi, D., et al. (2023). Integrated deep learning paradigm for document-based sentiment analysis. *Journal of King Saud University – Computer and Information Sciences*. 【support=0.75 | tier=0.6 | composite=0.725】

[9] Ali, J., Jusoh, A., Idris, N., et al. (2024). Healthcare service quality and patient satisfaction: a conceptual framework. *International Journal of Quality & Reliability Management*. 【support=0.65 | tier=0.6 | composite=0.775】

[10] Endeshaw, B. (2021). Healthcare service quality-measurement models: a review. *Journal of Health Research*. 【support=0.75 | tier=0.6 | composite=0.725】

[11] Lupo, T. (2016). A fuzzy framework to evaluate service quality in the healthcare industry: An empirical case of public hospital service evaluation in Sicily. *Applied Soft Computing*. 【support=0.85 | tier=0.8 | composite=0.695】

[12] Zhang, B., Hao, H., Zhan, Y., et al. (2026). How Physician Reviews Affect Online Consultation Demand: An Innovative Small Language Model with Fine-Tuning. *Information Systems Journal*. 【support=0.90 | tier=0.6 | composite=0.850】

[13] Antons, D., Breidbach, C.F., Joshi, A.M. (2023). Computational literature reviews: Method, algorithms, and roadmap. *Organizational Research Methods*. 【support=0.65 | tier=0.6 | composite=0.695】

[14] (2025). A probabilistic approach for building disease phenotypes across electronic health records. *BioData Mining*. 【support=0.75 | tier=0.1 | composite=0.655】

[15] Chang, J.E., Lindenfeld, Z., Albert, S.L., et al. (2021). Telephone vs. video visits during COVID-19: safety-net provider perspectives. *The Journal of the American Board of Family Medicine*. 【support=0.75 | tier=0.95 | composite=0.830】

[16] Andino, J.J., Eyrich, N.W., Boxer, R.J. (2023). Overview of telehealth in the United States since the COVID-19 public health emergency: a narrative review. *Mhealth*. 【support=0.95 | tier=0.6 | composite=0.785】

[17] Savira, F., Orellana, L., Hensher, M., et al. (2023). Use of general practitioner telehealth services during the COVID-19 pandemic in regional Victoria, Australia: retrospective analysis. *Journal of Medical Internet Research*. 【support=0.75 | tier=0.8 | composite=0.785】

[18] Olorunsogo, T.O., Balogun, O.D. (2024). Reviewing the evolution of US telemedicine post-pandemic by analyzing its growth, acceptability, and challenges in remote healthcare delivery. *World Journal of Clinical Cases*. 【support=0.75 | tier=0.6 | composite=0.805】

[19] (2025). Fig. 1 | Scientific Reports. *Scientific Reports*. 【support=0.75 | tier=0.1 | composite=0.655】

[20] Sharma, A., Pruthi, M., Sageena, G. (2022). Adoption of telehealth technologies: an approach to improving healthcare system. *Translational Medicine Communications*. 【support=0.65 | tier=0.6 | composite=0.695】

[21] Bettencourt, N., Wilson, C.J., Johnson, P.J. (2023). A rebalancing of financial valuations and expectations moving forward in the telehealth sector as the United States moves toward a post-COVID-19 reality. *Journal of Medical Internet Research*. 【support=0.65 | tier=0.8 | composite=0.755】

[22] Bestsennyy, O., Gilbert, G., Harris, A. (2021). Telehealth: a quarter-trillion-dollar post-COVID-19 reality. *McKinsey & Company*. 【support=0.75 | tier=0.2 | composite=0.605】

[23] Huang, X., Sun, P., Zhang, X., et al. (2024). What affects patients' choice of consultant: an empirical study of online doctor consultation service. *Electronic Commerce Research*. 【support=0.85 | tier=0.8 | composite=0.895】

[24] Guo, S., Wang, K., Yang, L., et al. (2025). Extending signaling theory in online health communities to address medical information asymmetry: systematic review with narrative synthesis. *Journal of Medical Internet Research*. 【support=0.90 | tier=0.8 | composite=0.910】

[25] Luo, A., Qin, L., Yuan, Y., et al. (2022). The effect of online health information seeking on physician-patient relationships: systematic review. *Journal of Medical Internet Research*. 【support=0.75 | tier=0.8 | composite=0.785】

[26] (2024). Examining the Role of Physician Characteristics in Web-Based Verified Primary Care Physician Reviews: Observational Study. 【support=0.75 | tier=0.1 | composite=0.655】

[27] Hong, Y.A., Liang, C., Radcliff, T.A., et al. (2019). What do patients say about doctors online? A systematic review of studies on patient online reviews. *Journal of Medical Internet Research*. 【support=0.90 | tier=0.8 | composite=0.710】

[28] Adams, S.A. (2010). Revisiting the online health information reliability debate in the wake of "web 2.0": an inter-disciplinary literature and website review. *International Journal of Medical Informatics*. 【support=0.85 | tier=0.8 | composite=0.615】

[29] Zhang, X., Sun, J., Li, X., et al. (2025). Developing a Framework for Online Review-Based Health Care Service Quality Assessment: Text-Mining Study. *Journal of Medical Internet Research*. 【support=0.95 | tier=0.8 | composite=0.925】

[30] Sehgal, N.K.R., Guntuku, S.C., Southwick, L. (2025). Online Reviews of Health Care Facilities. *JAMA Network Open*. 【support=0.88 | tier=0.8 | composite=0.904】

[31] Feizollah, A., Lin, C.Y., O'Malley, L., et al. (2025). The use of natural language processing to interpret unstructured patient feedback on health services: Scoping review. *Journal of Medical Internet Research*. 【support=0.85 | tier=0.8 | composite=0.895】

[32] Yan, J., Liang, C., Zhou, P. (2025). Physician's service quality and patient's review behavior: managing online review to attract more patients. *Internet Research*. 【support=0.75 | tier=0.8 | composite=0.865】

[33] Terpend, R., Rossetti, C., Kroes, J. (2025). Defining, measuring and managing healthcare quality using unstructured physician review comments. *The TQM Journal*. 【support=0.85 | tier=0.6 | composite=0.835】

[34] James, T.L., Calderon, E.D.V., Cook, D.F. (2017). Exploring patient perceptions of healthcare service quality through analysis of unstructured feedback. *Expert Systems with Applications*. 【support=0.85 | tier=0.8 | composite=0.695】

[35] Liu, Y., Agarwal, A., Lai, G., et al. (2026). On-demand healthcare platforms: Impact of question and answer service on online consultations and offline appointments. *Information Systems Journal*. 【support=0.85 | tier=0.6 | composite=0.835】

[36] Han, S., Li, L. (2024). Consulting doctors online after offline treatment: investigating the effects of online information on patients' effective use of online follow-up services. *Frontiers in Public Health*. 【support=0.75 | tier=0.6 | composite=0.805】

[37] Toit, J.D. (2024). Aspect-based sentiment analysis using topic modelling on student evaluations. 【support=0.65 | tier=0.8 | composite=0.835】

[38] Awadh, W.A., Sulaiman, R.B., Mahmoud, M.A. (2025). Aspect-based sentiment analysis in MOOCs: a systematic literature review introducing the MASC-MEF framework. *Journal of King Saud University – Computer and Information Sciences*. 【support=0.75 | tier=0.6 | composite=0.805】

[39] (2024). Aspect-Based Sentiment Analysis of Patient Feedback Using Large Language Models. 【support=0.90 | tier=0.1 | composite=0.700】

[40] Wilson, D., Moloney, E., Parr, J.M. (2021). Creating an Indigenous Māori‐centred model of relational health: A literature review of Māori models of health. *Journal of Clinical Nursing*. 【support=0.75 | tier=0.8 | composite=0.785】

[41] McCarthy, S., O'Raghallaigh, P. (2016). An integrated patient journey mapping tool for embedding quality in healthcare service reform. *Journal of Decision Systems*. 【support=0.85 | tier=0.6 | composite=0.635】

[42] Rawas, S., Tafran, C., AlSaeed, D. (2024). Transforming healthcare: AI-NLP fusion framework for precision decision-making and personalized care optimization in the era of IoMT. *Computers, Materials, & Continua*. 【support=0.85 | tier=0.8 | composite=0.895】

[43] Rahim, F., Hameed, N., Salih, S., et al. (2024). Natural language processing for healthcare: Applications, progress, and future directions. *Information and Technology*. 【support=0.70 | tier=0.95 | composite=0.895】

[44] Denecke, K., Reichenpfader, D. (2023). Sentiment analysis of clinical narratives: a scoping review. *Journal of Biomedical Informatics*. 【support=0.85 | tier=0.8 | composite=0.815】

[45] (2025). Developing a model for evaluating and improving the quality of healthcare services. *BMC Health Services Research*. 【support=0.65 | tier=0.1 | composite=0.625】

[46] (2025). Sustainable service quality assessment of Chinese healthcare e-government: a multi-criteria decision framework based on SERVQUAL model and entropy-weight TOPSIS method. *Frontiers*. 【support=0.65 | tier=0.1 | composite=0.625】

[47] Rosen, A.K., Rivard, P.E. (2025). Moving the needle on measurement of patient safety: the evolving role of the agency for healthcare research and quality (AHRQ) Patient safety indicators. *Joint Commission Journal on Quality and Patient Safety*. 【support=0.85 | tier=0.4 | composite=0.775】

[48] Mistry, K.B., Chesley, F.D. Jr., Chin, M.H. (2023). Advancing health equity‐agency for healthcare research and quality research and action agenda. *Health Services Research*. 【support=0.75 | tier=0.6 | composite=0.725】

[49] Damschroder, L.J., Aron, D.C., Keith, R.E., et al. (2009). Fostering implementation of health services research findings into practice: a consolidated framework for advancing implementation science. *Implementation Science*. doi:10.1186/1748-5908-4-50 【support=0.75 | tier=0.8 | composite=0.585】

[50] Ling, C., Zhao, X., Lu, J., et al. (2025). Domain specialization as the key to make large language models disruptive: A comprehensive survey. *ACM Computing Surveys*. 【support=0.75 | tier=0.95 | composite=0.910】

[51] Kumar, A. (2025). From Large to Small: The Rise of Small Language Models (SLMs) in Text Analytics. 【support=0.85 | tier=0.8 | composite=0.895】

[52] Wang, F., Zhang, Z., Zhang, X., et al. (2025). A comprehensive survey of small language models in the era of large language models: Techniques, enhancements, applications, collaboration with LLMs, and trustworthiness. *ACM Transactions on Intelligent Systems and Technology*. 【support=0.75 | tier=0.8 | composite=0.865】
