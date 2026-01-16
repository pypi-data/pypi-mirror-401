## LocRegen: Cost-Efficient Multilingual Product Title Optimization Using Small Language Models

## Anonymous ACL submission

## Abstract

E-commerce product titles often include redundant information that negatively impacts the user experience. Removing repetitive words through restructure and paraphrase can make titles more concise and informative. While large language models can optimize titles, their computational cost makes them impractical for large-scale applications. In this paper, we first analyze the sources of repetition in multilingual product titles, then present LocRegen, a system that uses smaller language models to efficiently remove redundancies while preserving essential product attributes. Our experiment across five languages shows LocRegen using 7B language model reduces redundant title rate to 2.4%, compared to 3.5% with a larger 12B baseline model. Additionally, LocRegen maintains a 3.8% error rate across all error categories including key attribute missing error, substantially outperforming the baseline's 8.4% error rate.

## 1 Introduction

With e-commerce shopping websites worldwide, products are accessible in different languages through global marketplaces. However, ecommerce catalogs (e.g., Amazon, Walmart) often contain products with excessively long titles that are difficult to read or exceed screen size limits (Zhang et al., 2021; Rozen et al., 2021). This leads to poor customer experience, particularly when titles are used in other contexts such as being read aloud by voice assistants. Studies show that 65% of product titles contain 15 or more words (Rozen et al., 2021), often intentionally lengthened by sellers who include redundant keywords and additional product attributes for search engine optimization (SEO) (Xiao and Munro, 2019).

The challenge is further complicated by modern e-commerce stores that enable multilingual product discovery (Rücklé et al., 2019; Nie, 2010; Saleh and Pecina, 2020; Bi et al., 2020; Jiang et al., 2020; Lowndes and Vasudevan, 2021) and localize product information using machine translation systems (Way, 2013; Guha and Heger, 2014; Zhou et al., 2018; Wang et al., 2021). Title length often increases during translation depending on the language pair (Zhang et al., 2024), necessitating additional optimization to improve customer experience by adhering to the Gricean maxim of quantity -being informative as required, no more and no less.

In industry settings, e-commerce product titles must conform to templates that specify key attributes for different product types. When optimizing titles, these essential attributes must be preserved. Removing repetitive words offers a safe and effective approach to such optimization. We define a repetitive word as one having more than two occurrences, and a redundant title as containing one or more repetitive words. The Repetitive Word Removal (RWR) task aims to reduce word occurrences to two or less (&lt;=2) through restructuring and paraphrasing while maintaining all key attributes, as shown below:

Original title : MASKED BRAND Large Desk Mat, Office Desk Pad, Computer Desk Mat, Laptop Mat for Desk, Desk Protector Mat, Desktop Mat, Desk Writing Pad, Desk Blotter Pad, Desk Cover Mat (80x40cm, Green)

Optimized title : MASKED BRAND Large Desk Mat for Office Computers, Laptops, and Desktops (80x40cm, Green)

The original title contains repetitive words Desk, Mat and Pad , which are reduced to fewer than 2 occurrences in the optimized version. The optimized title is shorter and more concise while retaining all key attributes for the desk mat product type including 'brand', 'product\_type', 'color' 'size'.

While multilingual large language models (LLMs) have shown promising results for summarization tasks and could potentially perform RWR through title regeneration, there are still major

challenges existing in the e-commerce context:

Cost and Scalability: Regenerating a large volume of multilingual titles using LLMs is costly and difficult to scale. While smaller language models offer lower costs, they typically show lower performance in preserving key attributes while removing duplicate words.

Dynamic Business Requirements: Title templates undergo frequent changes to accommodate business needs, either through refinements to existing product types or additions for new categories. This requires models to adapt quickly without extensive retraining.

Therefore, in this paper we first analyze redundancy in multilingual e-commerce titles, particularly focusing on how duplicate word(s) emerges during title localization, to determine optimal timing for repetitive word removal (RWR). Second, we propose LocRegen , a cost-efficient system that leverages a smaller language model for RWR through title regeneration. Our system consists of three key components: (1) dynamic feedback regeneration framework , (2) smart cue augmentation , and (3) a repetitive word detection system . These components enhance the small model's performance through iterative title regeneration and provide effective guidance for preserving key attributes while removing repetitive words.

Experiments across five languages show that LocRegen, using a 7B language model, reduces redundant title rate to 2.4%, compared to 3.5% with a larger 12B model. Additionally, LocRegen maintains a 3.8% error rate across all error categories including key attribute missing error, substantially outperforming the 12B model's 8.4% error rate, demonstrating its effectiveness as a practical, costefficient solution.

## 2 Redundancy in Multilingual E-commerce Titles

Our analysis reveals that while sellers may intentionally include repetitive words for marketing and search optimization, the localization process itself can naturally introduce additional redundancy. Table 1 shows that in our random experimental sample, a significant portion of non-redundant source titles become redundant after localization, with some language pairs reaching redundancy rates of up to 50

Table 1: The percentage of the e-commerce nonredundant source titles become redundant titles in the target language after localization. A product title is considered as redundant when it has one or more repetitive words (a word having more than two occurrences); We use random experimental data sample which has 100 to 10K titles per language pair.

| language pairs   | redund. rate   | language pairs     | redund. rate   |
|------------------|----------------|--------------------|----------------|
| German-Spanish   | 50%            | Italian-Spanish    | 25%            |
| German-English   | 46%            | Italian-Polish     | 25%            |
| Spanish-French   | 41%            | English-Polish     | 25%            |
| French-German    | 35%            | English-Italian    | 23%            |
| Italian-German   | 35%            | English-Spanish    | 22%            |
| Spanish-German   | 34%            | Spanish-Polish     | 20%            |
| French-Italian   | 32%            | English-French     | 19%            |
| Italian-English  | 32%            | Swedish-English    | 17%            |
| Italian-French   | 29%            | English-Swedish    | 14%            |
| Spanish-Italian  | 27%            | English-Dutch      | 13%            |
| Spanish-English  | 27%            | English-Portuguese | 13%            |
| English-German   | 27%            | Italian-Swedish    | 12%            |

## 2.1 Sources of Localization-Induced Repetitive words

Through extensive analysis of multilingual product titles, we have identified three primary mechanisms through which localization creates repetitive words:

## 2.1.1 Compound Word Decomposition

Languages such as German and Swedish naturally use compound words such the example below the Swedish word pö (rod) in compound words fiskespö , Spinnspö and saltvattensfiskespö . When translated into languages that do not use such compounds, like English, these words are typically split into their components, resulting in repetitive occurrences of words like Rod .

sv: [MASKED BRAND] Spinnspö lättvikts 24T kolfiberrämne slitstarkt fiskespö, premium korkhandtag, mångsidigt sötvattens-och saltvattensfiskespö för gädda, abborre och göstillgängliga i storlekar en: [MASKED BRAND] Spinning Rod Lightweight 24T Carbon Fiber Subject Heavy Duty Fishing Rod, Premium Cork Handle, Versatile Freshwater and Saltwater Fishing Rod for Pike, Perch and Zander-available in sizes

## 2.1.2 Vocabulary Asymmetry

Vocabulary asymmetry between languages can cause different source words to map to the same target word. Following (Nida and Taber, 1974)'s principle of functional equivalence in translation, this mapping often leads to repetition. For exam-

TITLE

TITLE

REG 1

Iterative generation loop

TITLE

TITLE

REG N-1

Redundant words r1

Prompt template 1

Redundant

REG Final

Redundant ple, the distinct English words Kids , Boys , Girls , and children may all translate to Kinder in German, which is correct but creating repetition in the target title. Feedback

LLM

en: [MASKED BRAND] Kids Animal costumes Boys Girls Pijamas Fancy Dress outfit Cosplay Children (Tiger, XL (For kids 120-140 cm tall))

de: [MASKED BRAND] Tierkostüme für Kinder, Jungen, Mädchen, Pyjama, Kostüm, Cosplay, Kinder (Tiger, XL (für Kinder 120-140 cm groß))

## 2.1.3 Morphological Richness Differences

Morphological differences between languages can create repetition when a source language's richer forms collapse into fewer target forms. For example, Italian distinguishes gender in nouns, with Neonato (masculine) and Neonata (feminine) both translating to Newborn in English, where grammatical gender doesn't exist. This morphological simplification in English leads to repetition in the translated text.

it: [MASKED BRAND] , Body Neonato e Neonata, Senza Manica, con Comoda Apertura a Patello, Designed in Italy, Abbigliamento Neonato e Neonata 0-24 Mesi, Idee Regalo Nascita en: [MASKED BRAND] , Newborn and Newborn Baby Bodysuit, Sleeveless, with Comfortable Snap-Button Opening Opening, Designed in Italy, Newborn and Newborn Clothing 0-24 Months, Birth Gift Ideas

## 3 LocRegen system

We formally define the Repetitive Words Removal (RWR) problem for e-commerce product titles as following: Given a product title t of product type P in language l , where t consists of a set of words W ( t ) = { w 1 , w 2 , ..., w i } and must preserve key product attributes A P = { a 1 , a 2 , ..., a m } specified by its product title template of product type P . We define redundancy R ( t ) as the set of repetitive words returned by a repetitive word Detector (RWD). The optimization objective is to generate a new title t ′ that minimizes the redundancy measure | R ( t ′ ) | while satisfying three essential constraints: (1) all key attributes A P present in the original title t must be preserved in t ′ , (2) t ′ must maintain grammatical correctness and semantic accuracy in language l , and (3) the regenerated title t ′ should be shorter than the original title | W ( t ′ ) | &lt; | W ( t ) | .

We propose a cost-efficient and effective title regeneration system LocRegen for Repetitive Words Removal (RWR) task. LocRegen uses a small language model, and it consists of three components: (1) Dynamic feedback Regeneration framework, (2)

Smart cues augmentation, (3) Multilingual Repetitive Word Detector (RWD).

## 3.1 Dynamic Feedback-aware Generation Framework

Figure 1: Feedback-aware generation framework

<!-- image -->

We propose Dynamic Feedback-aware generation as our core framework as Figure 1 illustrates. The feedback-aware generation framework iteratively regenerates redundant titles up to N rounds. At the end of each round (as well as before the first round), we employ a feedback generator, implemented as a repetitive word detector (RWD), to detect repetitive words still present in the regenerated title. When repetitive words are detected, indicating negative feedback, we collect these titles, update their prompts with information about the remaining repetitive words and the current regenerated title, and proceed to the next round of regeneration.

The iterative process continues regeneration and repetitive word detection until either no more repetitive words are detected or the maximum number of iterations is reached.

Figure 2: Dynamic feedback-aware title regeneration workflow

<!-- image -->

Multiple prompt templates : The difficulty of redundancy removal varies significantly across titles, product types, and languages. Additionally, redundancy removal is a delicate task requiring preservation of key attributes while minimizing unnecessary paraphrasing. Therefore, we introduce different prompt templates ranging from gentle to harsh instructions for repetitive word removal. With the dynamic feedback-aware generation framework, we can progressively adjust prompt templates as the process continues, as shown in Figure 2. We begin with vanilla prompts for the initial rounds and transition to more aggressive prompts for the final rounds, aligning prompt intensity with redundancy removal difficulty to maximize success.

## 3.2 Smart Cues Augmentation

Through analysis of regenerated titles, we observe that smaller language models tend to remove repetitive words from the beginning of titles, potentially eliminating crucial brand/product type information. This phenomenon becomes more pronounced when regenerating titles in certain languages. To address this, we introduce smart cues that reduce task difficulty and provide the base LLM with effective informational guidance. For repetitive word removal, we implement marker insertions ( [MARKER][/MARKER] ) around the first one or two occurrences of repetitive words from the beginning and include instructions not to remove marked words. This enables the LLM to focus on reducing repetitive words later in the title while preserving key attribute information. Those markers essentially reduce difficulty of the task by giving the model the guidance. Once the regeneration is complete, we remove all the markers in the regenerated titles. The following example with repetitive word 'balloons' demonstrates this approach:

Original Title: 10 Pack LED [MARKER] Balloons [/MARKER] Light Up [MARKER] Balloons [/MARKER] 20 Inches Clear Bobo Balloons, Helium Balloons Glow in the Dark Balloons, Warm White Party Balloons for Valentines Day Birthday Wedding Christmas Decoration

Regenerated Title: 10 Pack LED Balloons Light-Up Clear Bobo Balloons, 20 Inches, Helium-Filled Glow-in-the-Dark Party Decorations for Valentine's Day, Birthday, Wedding, Christmas

## 3.3 Repetitive Word Detector (RWD)

The multilingual Repetitive Word Detector (RWD) serves as the critical feedback generator in the

LocRegen system. As the RWD must process multilingual product titles from worldwide stores, it needs to handle morphologically rich languages where words can appear in different forms. Therefore, we employ lemmatization to obtain the base form of each word in the title for occurrences counting, and a base-form word with the occurrence over a threshold is considered as a repetitive word. Unlike word stemming, lemmatization produces actual words and requires understanding of word context while maintaining distinctions between different word meanings, making it more appropriate for language model processing.

The system also accounts for function words such as 'the', 'a' in English, 'el', 'la' in Spanish that serve grammatical roles. We leverage Partof-Speech (POS) tags to focus specifically on content words for repetitive word detection.

Additionally, product titles may contain brands and special expressions with legitimate repeated words. In such cases, we maintain a special expression cache to identify these instances and exclude them from repetitive word detection in the early stages.

## 4 Experimental Setup

Language Models: Qwen2.5-7B-Instruct 1 is used for LocRegen system. We also use Qwen2.5-1.5BInstruct 2 for analysis.

## Baseline:

1. Mistral-NeMo-12B 3 : uses Dynamic Iterative Feedback generation but 1 iteration with no smart cue augmentation.

2. LocRegen B : uses Dynamic Iterative Feedback generation up to 6 iterations with no smart cue augmentation.

Test Data: For each language, we have randomly sampled approximately 1K redundant titles across different product types from each of the e-commerce stores (DE, FR, IT, ES, UK).

Inference Optimization Empirically, we observe that near-greedy decoding yields better regeneration results for title redundancy removal.

1 https://huggingface.co/Qwen/Qwen2.5-7B-Instruct (Apache license 2.0)(Team, 2024)

2 https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct (Apache license 2.0) (Team, 2024)

3 https://huggingface.co/mistralai/Mistral-Nemo-Instruct2407 (Apache license 2.0)

Table 2: Manual audit error rate: Both LocRegen systems use the Qwen2.5-7B-Instruct , and maximum 6 iterations with 3 prompt templates. System LocRegen System B only uses only Dynamic Iterative Feedback generation without smart cue augmentation. Mistral-NeMo-12B uses same prompt but i iterations

|                  | LocRegen   | LocRegen   | LocRegen   | LocRegen   | LocRegen   | LocRegen B   | LocRegen B   | LocRegen B   | LocRegen B   | LocRegen B   | LocRegen B   | LocRegen B   | Mixtral NeMo   | Mixtral NeMo   | Mixtral NeMo   | Mixtral NeMo   | Mixtral NeMo   | Mixtral NeMo   |
|------------------|------------|------------|------------|------------|------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|----------------|----------------|----------------|----------------|----------------|----------------|
|                  | DE         | IT         | ES         | UK         | FR         | ave          | DE           | IT           | ES           | UK           | FR           | ave          | DE             | FR             | UK             | IT             | ES             | ave            |
| Redundancy       | 2.0%       | 1.6%       | 5.0%       | 2.0%       | 1.5%       | 2.4%         | 0.0%         | 4.0%         | 2.0%         | 0.0%         | 1.0%         | 1.4%         | 0.0%           | 1.5%           | 0.5%           | 7.0%           | 8.5%           | 3.5%           |
| Key Info Omitted | 0.5%       | 18.2%      | 8.5%       | 13.0%      | 17.1%      | 11.5%        | 1.0%         | 34.3%        | 45.2%        | 8.8%         | 17.8%        | 21.4%        | 4.5%           | 15.1%          | 17.0%          | 25.1%          | 5.5%           | 13.4%          |
| Hallucination    | 1.0%       | 1.5%       | 1.5%       | 5.5%       | 0.5%       | 2.0%         | 0.5%         | 5.1%         | 8.1%         | 6.2%         | 0.5%         | 4.1%         | 2.5%           | 2.5%           | 7.0%           | 14.6%          | 14.0%          | 8.1%           |
| Lingustic Errors | 0.0%       | 3.5%       | 0.0%       | 0.0%       | 0.5%       | 0.8%         | 0.0%         | 2.5%         | 7.6%         | 0.0%         | 1.0%         | 2.2%         | 2.5%           | 5.5%           | 0.0%           | 19.6%          | 15.5%          | 8.6%           |
| Context Change   | 1.0%       | 3.5%       | 1.0%       | 4.0%       | 1.5%       | 2.2%         | 7.2%         | 23.2%        | 29.4%        | 8.8%         | 11.2%        | 16.0%        | 6.5%           | 3.0%           | 7.5%           | 17.1%          | 7.5%           | 8.3%           |
| ave.             |            |            |            |            |            | 3.8%         |              |              |              |              |              | 9.0%         |                |                |                |                |                | 8.4%           |

Therefore, temperature is set as low as 0.1 for LLM inference. Near-greedy decoding also minimizes hallucination in generated titles. We use vllm 0.6.3.post1 4 as the inference framework

Repetitive Word Detector (RWD): we use spaCy-v3.6 5 for lemmatization and Part-ofSpeech tagging; For repetitive word detection, we exclude functional words with the following POS tags ADP, CCONJ, CARDINAL, SCONJ, DET, NUM , and special expressions such as brand names containing repetitive words; a lower-cased lemma has more than two occurrences (&gt;2) in the title is considered as a repetitive word

Dynamic Iterative generation: maximum 6 iterations: 3 iterations for the Vanilla prompt, 2 iterations for Mid-aggressive and 6th iteration for the Aggressive one, any experiments beyond 6th iteration uses aggressive prompt template. The regeneration process for a title can stop at any iteration if there is no repetitive words detected.

Progressive Prompt Templates: We implement three prompt templates with varying levels of aggressiveness for iterative generation. Each template incorporates (1) the original title or previous round's regenerated title(2) detected repetitive words and (3) product type-specific key attributes that must be preserved. The general instruction is to preserve the information of the attributes in the title template in the regeneration. The templates differ in their approach:

1. Vanilla prompt: Minimally restructures the title while preserving marked words and removing repetition
2. Mid-aggressive: Actively paraphrases and restructures while maintaining marked words

4 https://github.com/vllm-project/vllm (Apache-2.0 license)

5 https://github.com/explosion/spaCy (MIT License)

3. Aggressive: Prioritizes removing repetitive words, particularly towards the title's end

Metrics: When evaluating the performance of base small language models, we calculate redundant title rate using repetitive word detector (RWD).

We further conduct manual audit on the regenerated titles from LocRegen with the appropriate small langauge model ( Qwen2.5-7B-Instruct ) on the following aspects (1) Redundancy Present (Repetitive words are still present), (2) Key Information Omitted, (3) Hallucination Present, (4) Linguistic Errors Present, (5) Context Change Present. For (2) Key Information Omitted, we provide the auditors with list of the essential key attributes for each product type; the auditors can check whether any key attribute information in the original title for a given product type is missing in the regenerated titles.

## 5 Results and Analysis

## 5.1 Select the proper smaller language model for LocRegen system

We have conducted experiments with two variants of the Qwen2.5 model family-the 7B and 1.5B parameter versions using much larger test sets we sampled from the traffic - to (1) evaluate the base model repetitive word removal performance, (2) investigate the smaller model size affects the iterative regeneration process. The 7B model reduces redundancy title rate from an initial average of 32.7% to 1.8% within 6 iterations. The improvement is particularly notable in the early rounds, with the largest reduction occurring between rounds 1 and 2 (32.7% to 17.0%). The model shows consistent performance across all languages. In comparison, the smaller 1.5B model reduces the redundancy title rate to 16-17% after round 6, with minimal improvements in subsequent iterations. This plateau effect is consistent across all languages, suggesting a limitation in the model's capacity to further optimize the titles. The 7B ( Qwen2.5-7B-Instruct )

is more proper for our task. Tables 3 and 4 in Appendix show the percentage of redundant titles detected by RWD across multiple iteration rounds for each model.

## 5.2 Regenerated title quality

Table 2 shows the manual audit results. We use Mixtral-NeMo-12B model (with one iteration regeneration) to serves as a strong baseline. LocRegen , implementing both Dynamic Iterative Feedback generation and Smart cues augmentation, outperforms the larger Mixtral-NeMo-12B across all error categories: achieves notably lower average error rates in hallucinations (2.0% vs 8.1%), linguistic errors (0.8% vs 8.6%), and context changes (2.2% vs 8.3%). This better performance is particularly significant given that LocRegen accomplishes this with substantially fewer parameters. Our analysis as Table 5 in Appendix shows the length of regenerated titles is reduced approximately 30% on average across 5 languages, while preserving essential information.

LocRegen B performing better in some categories (hallucinations: 4.1% vs 8.1%) but worse in others (key information omission: 21.4% vs 13.4%). This suggests that the iterative feedback mechanism alone, without smart cues augmentation, may not be sufficient to consistently outperform larger models. These result demonstrates that our proposed approaches in LocRegen can effectively overcome the limitations of model size offering a more efficient approach to effectively remove the repetitive words in product titles while preserving the key attribute information.

## 6 Related work

In an industry setting, Repetitive Words Removal (RWR) task for product titles is typically conducted through a title length optimization step, which employs techniques such as monolingual summarization (Sun et al., 2018; Fetahu et al., 2023), text truncation (Wang et al., 2020; Guan et al., 2022) and manual editing. These approaches focus primarily on reducing title length while attempting to preserve key information, though they may not explicitly target redundancy. Recent work has explored neural models for product title optimization, including masked text scoring (Samar et al., 2018) and user-sensitive adversarial training (Wang et al., 2020). While these approaches show promise, they typically require significant training data and computational resources. The multilingual title length problem has also been studied in the context of localization (Zhang et al., 2024) which analyzes how product title length increases during the localization process and conducted comparative studies using large language models versus small encoder-decoder transfer models for title optimization. However, their focus is on general title summarization rather than specifically addressing redundancy while preserving key product attributes from title templates. Other approach utilizes product title templates to structure information (Xiao and Munro, 2019), though primarily for title generation rather than redundancy removal. To our knowledge, our work is the first to specifically address multilingual product title redundancy through a cost-efficient approach that: 1) explicitly preserves template-specified key attributes, 2) leverages small language models with specialized augmentation techniques, and 3) provides an iterative feedback mechanism for precise redundancy removal across languages.

## 7 Conclusion

In this paper, we first analyze redundancy in multilingual e-commerce titles, particularly focusing on how repetitive words emerge during title localization, then we present LocRegen, a cost-efficient system for reducing redundancy in multilingual ecommerce product titles using small language models. By combining Dynamic Feedback-aware generation, Smart Cues Augmentation, and a Multilingual Repetitive Word Detector, our system enables a smaller language model to outperform a much larger baseline language model. Human evaluation demonstrates that LocRegen, using a 7B parameter model, achieves better results than much larger model while maintaining consistent title length reductions of 27.5-32.1% across languages. These results show that complex NLP tasks can be accomplished efficiently with smaller models when enhanced with appropriate techniques.

## 8 Limitations and Future Work

While LocRegen demonstrates strong performance in redundancy removal, several limitations should be noted. First, our system has only been tested on five European languages with similar linguistic structures; its effectiveness on languages with significantly different characteristics (such as Asian languages or right-to-left scripts) remains unknown.

Second, the current redundancy detection approach relies heavily on word-level analysis, which may not capture more subtle semantic redundancies or context-dependent cases. Third, while our Smart Cues Augmentation helps preserve key product information, it may not fully address complex cases where attribute importance varies by product category or market. These limitations suggest opportunities for future research in expanding language coverage, developing more sophisticated redundancy detection methods, and creating more adaptive title optimization strategies.

## References

Tianchi Bi, Liang Yao, Baosong Yang, Haibo Zhang, Weihua Luo, and Boxing Chen. 2020. Constraint translation candidates: A bridge between neural query translation and cross-lingual information retrieval. Preprint, arXiv:2010.13658.

Besnik Fetahu, Zhiyu Chen, Oleg Rokhlenko, and Shervin Malmasi. 2023. InstructPTS: Instructiontuning LLMs for product title summarization. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: Industry Track, pages 663-674, Singapore. Association for Computational Linguistics.

Xinyi Guan, Shun Long, Weiheng Zhu, Silei Cao, and Fangting Liao. 2022. Mask-based text scoring for product title summarization. In 2022 8th International Conference on Systems and Informatics (ICSAI), pages 1-6.

Jyoti Guha and Carmen Heger. 2014. Machine translation for global e-commerce on ebay. In Proceedings of the AMTA, volume 2, pages 31-37.

Zhuolin Jiang, Amro El-Jaroudi, William Hartmann, Damianos Karakos, and Lingjun Zhao. 2020. Crosslingual information retrieval with BERT. In Proceedings of the workshop on Cross-Language Search and Summarization of Text and Speech (CLSSTS2020), pages 26-31, Marseille, France. European Language Resources Association.

Mike Lowndes and Aditya Vasudevan. 2021. Market guide for digital commerce search.

Eugene Albert Nida and Charles Russell Taber. 1974. The theory and practice of translation, volume 8. Brill Archive.

Jian-Yun Nie. 2010. Cross-language information retrieval. Synthesis Lectures on Human Language Technologies, 3(1):1-125.

Ohad Rozen, David Carmel, Avihai Mejer, Vitaly Mirkis, and Yftah Ziser. 2021. Answering productquestions by utilizing questions from other contextually similar products. In Proceedings of the 2021

Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pages 242-253, Online. Association for Computational Linguistics.

Andreas Rücklé, Krishnkant Swarnkar, and Iryna Gurevych. 2019. Improved cross-lingual question retrieval for community question answering. In The World Wide Web Conference, WWW '19, page 3179-3186, New York, NY, USA. Association for Computing Machinery.

Shadi Saleh and Pavel Pecina. 2020. Document translation vs. query translation for cross-lingual information retrieval in the medical domain. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 6849-6860, Online. Association for Computational Linguistics.

Thaer Samar, Myriam C. Traub, Jacco Ossenbruggen, Lynda Hardman, and Arjen P. Vries. 2018. Quantifying retrieval bias in web archive search. Int. J. Digit. Libr., 19(1):57-75.

Fei Sun, Peng Jiang, Hanxiao Sun, Changhua Pei, Wenwu Ou, and Xiaobo Wang. 2018. Multi-source pointer network for product title summarization. In Proceedings of the 27th ACM International Conference on Information and Knowledge Management, CIKM '18, page 7-16, New York, NY, USA. Association for Computing Machinery.

Haifeng Wang, Hua Wu, Zhongjun He, Liang Huang, and Kenneth Ward Church. 2021. Progress in machine translation. Engineering.

Manyi Wang, Tao Zhang, Qijin Chen, and Chengfu Huo. 2020. Selling products by machine: a user-sensitive adversarial training method for short title generation in mobile e-commerce.

Andy Way. 2013. Traditional and emerging use-cases for machine translation. Proceedings of Translating and the Computer, 35:12.

Joan Xiao and Robert Munro. 2019. Text summarization of product titles. In eCOM@SIGIR.

Bryan Zhang, Taichi Nakatani, Daniel Vidal Hussey, Stephan Walter, and Liling Tan. 2024. Don't just translate, summarize too: Cross-lingual product title generation in E-commerce. In Proceedings of the Seventh Workshop on e-Commerce and NLP @ LREC-COLING 2024, pages 58-64, Torino, Italia. ELRA and ICCL.

Xueying Zhang, Yunjiang Jiang, Yue Shang, Zhaomeng Cheng, Chi Zhang, Xiaochuan Fan, Yun Xiao, and Bo Long. 2021. Dsgpt: Domain-specific generative pre-training of transformers for text generation in e-commerce title and review summarization. In Proceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval, SIGIR '21, page 2146-2150, New York, NY, USA. Association for Computing Machinery.

Mingyang Zhou, Runxiang Cheng, Yong Jae Lee, and Zhou Yu. 2018. A visual attention grounding neural model for multimodal machine translation. CoRR, abs/1808.08266.

## A Small language performance comparison to remove duplicate words in titles

Table 3: LocRegen with base model Qwen2.5-7Binstruct . The percentage of redundant title detected by the repetitive word detector (RWD) during each round of the feedback-aware iterative regeneration, each language has 1K titles

|      | r1    | r2    | r3    | r4    | r5   | r6   |
|------|-------|-------|-------|-------|------|------|
| DE   | 28.6% | 16.5% | 12.7% | 11.1% | 7.1% | 1.8% |
| FR   | 32.1% | 16.6% | 11.4% | 9.6%  | 6.3% | 1.6% |
| IT   | 32.0% | 15.3% | 11.0% | 9.5%  | 6.2% | 2.2% |
| ES   | 29.4% | 13.9% | 9.3%  | 4.8%  | 3.9% | 0.8% |
| UK   | 41.1% | 22.7% | 18.2% | 16.1% | 9.7% | 2.7% |
| Aver | 32.7% | 17.0% | 12.5% | 10.2% | 6.6% | 1.8% |

Table 4: LocRegen with base model Qwen2.5-1.5B-instruct . The percentage of redundant title detected by the repetitive word detector (RWD) during each round of the feedback-aware iterative regeneration, each language has 1K titles

|      | r1   | r2   | r3   | r4   | r5   | r6   | r7   | r8   | r9   |
|------|------|------|------|------|------|------|------|------|------|
| DE   | 36%  | 23%  | 19%  | 19%  | 18%  | 18%  | 18%  | 17%  | 17%  |
| FR   | 43%  | 27%  | 21%  | 19%  | 18%  | 17%  | 17%  | 17%  | 17%  |
| IT   | 39%  | 24%  | 20%  | 18%  | 17%  | 17%  | 17%  | 16%  | 16%  |
| ES   | 40%  | 23%  | 19%  | 17%  | 16%  | 15%  | 15%  | 15%  | 15%  |
| UK   | 47%  | 25%  | 19%  | 18%  | 17%  | 17%  | 17%  | 17%  | 17%  |
| Aver | 41%  | 25%  | 20%  | 18%  | 17%  | 17%  | 17%  | 16%  | 16%  |

## B Title length reduction

Table 5: Percentage reduction in title length between original and regenerated titles across languages. Values show both median and mean reductions, measured in characters. Negative percentages indicate shorter regenerated titles.

| Language   | ∆ Median (%)   | ∆ Mean (%)   |
|------------|----------------|--------------|
| FR         | -34.8%         | -31.4%       |
| IT         | -36.5%         | -32.1%       |
| ES         | -32.1%         | -29.6%       |
| EN         | -32.1%         | -27.5%       |
| DE         | -32.1%         | -29.2%       |

As repetitive word removal in titles can intuitively optimize title length, we further investigate the title length reduction. Table 5 shows consistent title length reductions across all five languages, with mean reductions ranging from 27.5% to 32.1% and median reductions from 32.1% to 36.5%. Italian and French demonstrate the strongest compression rates (mean reductions of 32.1% and 31.4% respectively), while English shows a more moderate 27.5% reduction. These consistent results across different languages demonstrate LocRegen 's effectiveness in reducing title length while preserving essential information.