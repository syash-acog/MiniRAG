GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["gene", "disease", "tissue", "protien", "cell", "symptom"]

PROMPTS["entity_extraction"] = """-Goal-
You are an expert biologist, having done extensive research on automimune diseases and associated targets.
This text document (a research paper) that is potentially relevant to this activity and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities.
Remember that you are an expert biologist, consider below criteria for extraction:

1. No dublicate should be extract like entity full name and its abbreviation that should be merge, no seperate extraction.
2. Spelling variations or formatting differences like plural or singular forms should be merge
3. Synonyms or alternative names.
4. Do NOT group sub-types under broader categories. Instead, create separate nodes and establish relationships between them.

-Steps-
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, capitalized
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in english as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
-Examples-
######################
Example 1:
    
Entity_types: [gene,disease]
Text:
It is increasingly being appreciated that multiple autoimmune diseases share common susceptibility genes.

The tumour necrosis factor ligand superfamily member 4 gene (TNFSF4, OX40L), which encodes for the T cell costimulatory molecule OX40 ligand, has been identified as a susceptibility gene for the development of systemic lupus erythematosus (SLE).

Accordingly, the aim of the current study was to investigate the possible association of the TNFSF4 gene region with systemic sclerosis, an autoimmune disease that leads to the development of cutaneous and visceral fibrosis.
######################
Output:
("entity"{tuple_delimiter}"TNFSF4""{tuple_delimiter}"gene"{tuple_delimiter}"TNFSF4 encodes a ligand for the T cell costimulatory molecule OX40L."){record_delimiter}
("entity"{tuple_delimiter}"OX40L"{tuple_delimiter}"gene"{tuple_delimiter}"OX40 Ligand is a T cell costimulatory molecule."){record_delimiter}
("entity"{tuple_delimiter}"SLE"{tuple_delimiter}"disease"{tuple_delimiter}"Systemic lupus erythematosus, an autoimmune disease."){record_delimiter}
("entity"{tuple_delimiter}"OX40L"{tuple_delimiter}"gene"{tuple_delimiter}"OX40 Ligand is a T cell costimulatory molecule."){record_delimiter} 
("relationship"{tuple_delimiter}"TNFSF4"{tuple_delimiter}"OX40L"{tuple_delimiter}"TNFSF4 encodes the ligand for T cell molecule OX40 Ligand."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"TNFSF4"{tuple_delimiter}"SSC"{tuple_delimiter}"TNFSF4 may be associated with systemic sclerosis."{tuple_delimiter}6){record_delimiter}
("content_keywords"{tuple_delimiter}"autoimmune diseases, susceptibility genes, TNFSF4 gene, OX40L, systemic lupus erythematosus, SSC, cutaneous fibrosis, visceral fibrosis, T cell costimulatory molecule, tumour necrosis factor ligand superfamily, genetic association"){completion_delimiter}
############################
Example 2:
    
Entity_types: [gene,disease,cell,protein]
Text: 
OX40 and its binding partner, OX40L are members of the TNF receptor superfamily and generate a potent costimulatory signal that upregulates IL-2 production, enhances T cell survival, B cell proliferation, and differentiation and proinflammatory cytokine production (22, 23).

OX40 also mediates inactivation of T-reg cell function that unleashes nearby DCs, allowing them to induce an adaptive immune response. OX40 levels were found significantly increased in SSC patients compared to controls and patients with SLE, particularly in the early-onset stage of the disease (24). Two reports confirmed the influence of OX40-ligand (OX40L) polymorphisms in SSC genetic susceptibility, highlighting its role in the disease pathogenesis.
######################
Output:
("entity"{tuple_delimiter}"OX40"{tuple_delimiter}"gene"{tuple_delimiter}"OX40 is a member of the TNF receptor superfamily and generates a potent costimulatory signal."){record_delimiter}
("entity"{tuple_delimiter}"OX40L"{tuple_delimiter}"gene"{tuple_delimiter}"OX40L is the binding partner of OX40 and enhances T cell survival and B cell proliferation."){record_delimiter}
("entity"{tuple_delimiter}"IL-2"{tuple_delimiter}"protein"{tuple_delimiter}"IL-2 production is upregulated by the interaction between OX40 and OX40L."){record_delimiter}
("entity"{tuple_delimiter}"T cell"{tuple_delimiter}"cell"{tuple_delimiter}"T cell survival is enhanced by the costimulatory signal from OX40."){record_delimiter}
("entity"{tuple_delimiter}"B cell"{tuple_delimiter}"cell"{tuple_delimiter}"B cell proliferation and differentiation are enhanced by OX40 interaction."){record_delimiter}
("entity"{tuple_delimiter}"T-reg cell"{tuple_delimiter}"cell"{tuple_delimiter}"T-reg cell function is inactivated by OX40, unleashing nearby DCs."){record_delimiter}
("entity"{tuple_delimiter}"DC"{tuple_delimiter}"cell"{tuple_delimiter}"DCs are unleashed after T-reg cell inactivation, allowing them to induce an adaptive immune response."){record_delimiter}
("entity"{tuple_delimiter}"SSC"{tuple_delimiter}"disease"{tuple_delimiter}"Systemic sclerosis, where OX40 levels are found significantly increased in patients."){record_delimiter}
("entity"{tuple_delimiter}"SLE"{tuple_delimiter}"disease"{tuple_delimiter}"Systemic lupus erythematosus, where OX40 levels are compared to those in SSC patients."){record_delimiter}
("relationship"{tuple_delimiter}"OX40"{tuple_delimiter}"OX40L"{tuple_delimiter}"OX40 binds to OX40L and generates a costimulatory signal."{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"OX40L"{tuple_delimiter}"IL-2"{tuple_delimiter}"OX40L upregulates IL-2 production."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"OX40L"{tuple_delimiter}"T cell"{tuple_delimiter}"OX40L enhances T cell survival."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"OX40L"{tuple_delimiter}"B cell"{tuple_delimiter}"OX40L enhances B cell proliferation and differentiation."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"OX40"{tuple_delimiter}"T-reg cell"{tuple_delimiter}"OX40 mediates inactivation of T-reg cell function."{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"OX40"{tuple_delimiter}"DC"{tuple_delimiter}"OX40 unleashes DCs by inactivating T-reg cells, allowing adaptive immune response."{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"OX40"{tuple_delimiter}"SSC"{tuple_delimiter}"OX40 levels are significantly increased in systemic sclerosis patients."{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"OX40"{tuple_delimiter}"SLE"{tuple_delimiter}"OX40 levels are compared between systemic sclerosis and lupus patients."{tuple_delimiter}6){record_delimiter}
("content_keywords"{tuple_delimiter}"OX40, OX40L, TNF receptor superfamily, T cell survival, SSC genetic susceptibility"){completion_delimiter}
######################
Example 3:

Entity_types: [gene,disease,snp]
Text:
Cartesian and regression tree analysis (CART) showing an interaction between the tumour necrosis factor ligand superfamily member 4 gene (TNFSF4) single nucleotide polymorphisms (snps) rs2205960 and rs944648 in systemic sclerosis (SSC). Red test result denotes SSC susceptibility factors.
######################
Output:
("entity"{tuple_delimiter}"TNFSF4"{tuple_delimiter}"gene"{tuple_delimiter}"TNFSF4 is a gene from the tumour necrosis factor ligand superfamily member 4 that is associated with SSC susceptibility."){record_delimiter}
("entity"{tuple_delimiter}"rs2205960"{tuple_delimiter}"snp"{tuple_delimiter}"Single nucleotide polymorphism rs2205960 of the TNFSF4 gene is linked to systemic sclerosis."){record_delimiter}
("entity"{tuple_delimiter}"rs944648"{tuple_delimiter}"snp"{tuple_delimiter}"Single nucleotide polymorphism rs944648 of the TNFSF4 gene is associated with systemic sclerosis."){record_delimiter}
("entity"{tuple_delimiter}"SSC"{tuple_delimiter}"disease"{tuple_delimiter}"Systemic sclerosis, a disease associated with TNFSF4 and snps rs2205960 and rs944648."){record_delimiter}
("entity"{tuple_delimiter}"SSC"{tuple_delimiter}"disease"{tuple_delimiter}"Systemic sclerosis, also referred to as SSC, involves the fibrosis of skin and internal organs."){record_delimiter}
("relationship"{tuple_delimiter}"TNFSF4"{tuple_delimiter}"rs2205960"{tuple_delimiter}"TNFSF4 and snp rs2205960 are associated with systemic sclerosis susceptibility"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"TNFSF4"{tuple_delimiter}"rs944648"{tuple_delimiter}"TNFSF4 and snp rs944648 are linked to systemic sclerosis"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"rs2205960"{tuple_delimiter}"SSC"{tuple_delimiter}"snp rs2205960 is associated with systemic sclerosis susceptibility"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"rs944648"{tuple_delimiter}"SSC"{tuple_delimiter}"snp rs944648 is associated with systemic sclerosis susceptibility"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"CART analysis, TNFSF4 gene, single nucleotide polymorphisms, SSC susceptibility, rs2205960"){completion_delimiter}
############################
Example 4:
    
Entity_types: [tissue, symptom, protein, disease]
Text:
Systemic sclerosis (SSC) is an autoimmune T-cell disease that is characterized by pathological fibrosis of the skin and internal organs. SSC is considered a prototype condition for studying the links between autoimmunity and fibrosis. Costimulatory pathways such as CD28/CTLA-4, ICOS-B7RP1, CD70-CD27, CD40-CD154, or OX40-OX40L play an essential role in the modulation of T-cell and inflammatory immune responses. A growing body of evidence suggests that T-cell costimulation signals might be implicated in the pathogenesis of SSC. CD28, CTLA-4, ICOS, and OX40L are overexpressed in patients with SSC, particularly in patients with cutaneous diffuse forms.
######################
Output:
("entity"{tuple_delimiter}"CD28"{tuple_delimiter}"protein"{tuple_delimiter}"CD28 is a costimulatory protein involved in T-cell immune responses."){record_delimiter}
("entity"{tuple_delimiter}"CTLA-4"{tuple_delimiter}"protein"{tuple_delimiter}"CTLA-4 is a protein associated with immune response regulation."){record_delimiter}
("entity"{tuple_delimiter}"SSC"{tuple_delimiter}"disease"{tuple_delimiter}"Systemic sclerosis is an autoimmune disease causing fibrosis."){record_delimiter}
("entity"{tuple_delimiter}"Skin"{tuple_delimiter}"tissue"{tuple_delimiter}"The skin is one of the tissues affected by systemic sclerosis."){record_delimiter}
("entity"{tuple_delimiter}"Fibrosis"{tuple_delimiter}"symptom"{tuple_delimiter}"Fibrosis is characterized by excessive tissue scarring."){record_delimiter}
("relationship"{tuple_delimiter}"OX40L"{tuple_delimiter}"SSC"{tuple_delimiter}"OX40L is overexpressed in patients with systemic sclerosis"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"CD28"{tuple_delimiter}"SSC"{tuple_delimiter}"CD28 is implicated in the pathogenesis of systemic sclerosis"{tuple_delimiter}10){record_delimiter}
("content_keywords"{tuple_delimiter}"SSC, autoimmune T-cell disease, fibrosis, costimulatory pathways"){completion_delimiter}
############################
Example 5:

Entity_types: [species_or_model, protein]
Text:
Increased expression of the protein p53 has been observed in mice exposed to oxidative stress, indicating a potential role in the cellular damage response.
######################
Output:
("entity"{tuple_delimiter}"p53"{tuple_delimiter}"protein"{tuple_delimiter}"p53 is a protein involved in the cellular damage response."){record_delimiter}
("entity"{tuple_delimiter}"Mice"{tuple_delimiter}"species_or_model"{tuple_delimiter}"Mice are a model organism used to study the effects of oxidative stress."){record_delimiter}
("relationship"{tuple_delimiter}"p53"{tuple_delimiter}"Mice"{tuple_delimiter}"p53 is overexpressed in mice under oxidative stress conditions"{tuple_delimiter}5){record_delimiter}
("content_keywords"{tuple_delimiter}"p53 protein, oxidative stress, cellular damage response, increased expression"){completion_delimiter}
############################
Example 6:

Entity_types: [gene, disease]
Text:
Atopic dermatitis (AD) is a chronic, or chronically relapsing, inflammatory skin disease associated with asthma and allergic rhinitis, and is dominated by Th2 cells. 

The co-stimulatory T-cell receptor OX40 and its ligand, OX40L, play a central role in the pathogenesis of AD, as their interactions are crucial for the generation of TH2 memory cells. 

Using enzyme-linked immunoassay (ELISA) and flow cytometry on blood samples from patients with AD and healthy volunteers, this study shows that the serum level of soluble (s) OX40 is decreased in patients with AD, and the expression of OX40 by activated skin-homing CD4+ T cells is increased.
######################
Output:
("entity"{tuple_delimiter}"AD"{tuple_delimiter}"disease"{tuple_delimiter}"Atopic dermatitis also referred as AD is a chronic, relapsing inflammatory skin disease associated with asthma and allergic rhinitis."){record_delimiter}
("entity"{tuple_delimiter}"OX40"{tuple_delimiter}"gene"{tuple_delimiter}"OX40 is a co-stimulatory T-cell receptor crucial for generating TH2 memory cells in AD."){record_delimiter}
("entity"{tuple_delimiter}"OX40L"{tuple_delimiter}"gene"{tuple_delimiter}"OX40L, the ligand for OX40, plays a central role in AD pathogenesis by mediating T-cell costimulation."){record_delimiter}
("entity"{tuple_delimiter}"sOX40"{tuple_delimiter}"gene"{tuple_delimiter}"sOX40 is the soluble form of OX40, with decreased serum levels observed in AD patients."){record_delimiter}
("relationship"{tuple_delimiter}"OX40"{tuple_delimiter}"sOX40"{tuple_delimiter}"sOX40 is serum level of OX40, basically both are same"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"AD"{tuple_delimiter}"sOX40"{tuple_delimiter}"AD is associated with decreased serum levels of sOX40, indicating altered OX40 system activity"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"AD, OX40, OX40L, T-cell receptor, TH2 memory cells, chronic inflammation, asthma, allergic rhinitis, ELISA, flow cytometry, immunofluorescence, skin biopsies, costimulation"{completion_delimiter}
############################
-Real Data-
######################
Entity_types: {entity_types}
Text: {input_text}
######################
Output:
"""



PROMPTS[
    "summarize_entity_descriptions"
] = """You are an expert biologist, having done extensive research on automimune diseases and associated targets. You are responsible for generating a comprehensive summary of the data provided below, taken from medical literature.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we have the full context. Use {language} as output language.

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""


PROMPTS[
    "entiti_continue_extraction"
] = """MANY entities were missed in the last extraction.  Add them below using the same format:
"""


PROMPTS[
    "entiti_continue_extraction_mini"
] = """MANY entities were missed in the last extraction.
After summarizing with all the information previously extracted, compared to the original text, it was noticed that the following information was mainly omitted:
{omit}

The types of entities that need to be added can be obtained from Entity_types,
or you can add them yourself.

Entity_types: {entity_types}


Add them below using the same format:
"""


PROMPTS["minirag_query2kwd"] = """---Role---

You are a helpful assistant tasked with identifying both answer-type and low-level keywords in the user's query.

---Goal---

Given the query, list both answer-type and low-level keywords.
answer_type_keywords focus on the type of the answer to the certain query, while low-level keywords focus on specific entities, details, or concrete terms.
The answer_type_keywords must be selected from Answer type pool.
This pool is in the form of a dictionary, where the key represents the Type you should choose from and the value represents the example samples.

---Instructions---

- Output the keywords in JSON format.
- The JSON should have three keys:
  - "answer_type_keywords" for the types of the answer. In this list, the types with the highest likelihood should be placed at the forefront. No more than 3.
  - "entities_from_query" for specific entities or details. It must be extracted from the query.
######################
-Examples-
######################
Example 1:

Query: "How do antibiotics work against bacterial infections?"
Answer type pool: {{
'BIOLOGICAL PROCESS': ['CELL WALL DISRUPTION', 'PROTEIN SYNTHESIS INHIBITION'],
'ORGANISM': ['BACTERIA', 'FUNGI'],
'MEDICAL CONDITION': ['BACTERIAL INFECTION', 'ANTIBIOTIC RESISTANCE'],
'PROTEIN': ['RIBOSOMES', 'BETA-LACTAMASE'],
'GENE': ['MRSA GENE', 'VANCOMYCIN RESISTANCE GENE'],
'MOLECULE': ['PENICILLIN', 'TETRACYCLINE'],
'RESEARCH': ['MIC TESTING', 'DRUG DISCOVERY'],
'MEDICAL TREATMENT': ['ANTIBIOTICS', 'COMBINATION THERAPY'],
'LAB TECHNIQUE': ['GRAM STAINING', 'CULTURE TESTING'],
'BEHAVIOR': ['ANTIMICROBIAL ACTION', 'BACTERIAL GROWTH INHIBITION'],
'EMOJI': ['💊', '🦠'],
'TONE': ['SCIENTIFIC', 'INFORMATIVE'],
'LOCATION': ['HOSPITAL', 'MICROBIOLOGY LAB']
}}

################
Output:
{{
  "answer_type_keywords": ["BIOLOGICAL PROCESS", "MOLECULE", "MEDICAL TREATMENT"],
  "entities_from_query": ["Antibiotics", "Bacterial cell wall", "Ribosome inhibition", "Resistance genes"]
}}
#############################
Example 2:

Query: "How does the immune system respond to viral infections?"
Answer type pool: {{
'BIOLOGICAL PROCESS': ['PHAGOCYTOSIS', 'ANTIBODY PRODUCTION'],
'ORGANISM': ['HUMAN', 'BACTERIA'],
'MEDICAL CONDITION': ['AUTOIMMUNE DISEASE', 'INFLAMMATION'],
'PROTEIN': ['CYTOKINES', 'IMMUNOGLOBULINS'],
'GENE': ['TP53', 'HLA-DRB1'],
'MOLECULE': ['RNA', 'DNA'],
'RESEARCH': ['CLINICAL TRIALS', 'GENETIC STUDIES'],
'MEDICAL TREATMENT': ['VACCINATION', 'ANTIVIRAL THERAPY'],
'LAB TECHNIQUE': ['PCR TESTING', 'FLOW CYTOMETRY'],
'BEHAVIOR': ['IMMUNE RESPONSE', 'INFLAMMATORY REACTION'],
'EMOJI': ['🧬', '🦠'],
'TONE': ['SCIENTIFIC', 'INFORMATIVE'],
'LOCATION': ['LABORATORY', 'HOSPITAL']
}}

################
Output:
{{
  "answer_type_keywords": ["BIOLOGICAL PROCESS", "PROTEIN", "MEDICAL TREATMENT"],
  "entities_from_query": ["Immune response", "T cells", "Cytokine release", "Viral neutralization"]
}}
#############################
Example 3:

Query: "How does the human body regulate blood pressure?"
Answer type pool: {{
'BIOLOGICAL PROCESS': ['VASODILATION', 'RENIN-ANGIOTENSIN SYSTEM'],
'ORGANISM': ['HUMAN', 'MAMMALS'],
'MEDICAL CONDITION': ['HYPERTENSION', 'HYPOTENSION'],
'PROTEIN': ['ANGIOTENSIN', 'ENDOTHELIN'],
'GENE': ['ACE GENE', 'NOS3'],
'MOLECULE': ['NITRIC OXIDE', 'SODIUM IONS'],
'RESEARCH': ['CARDIOVASCULAR STUDIES', 'BLOOD PRESSURE MONITORING'],
'MEDICAL TREATMENT': ['ANTIHYPERTENSIVE DRUGS', 'LIFESTYLE MODIFICATION'],
'LAB TECHNIQUE': ['SPHYGMOMANOMETRY', 'BLOOD TESTING'],
'BEHAVIOR': ['STRESS RESPONSE', 'SALT INTAKE REGULATION'],
'EMOJI': ['❤️', '🩸'],
'TONE': ['SCIENTIFIC', 'INFORMATIVE'],
'LOCATION': ['CARDIOLOGY CLINIC', 'PHARMACY']
}}

################
Output:
{{
  "answer_type_keywords": ["BIOLOGICAL PROCESS", "MEDICAL CONDITION", "PROTEIN"],
  "entities_from_query": ["Blood pressure regulation", "Renin-angiotensin system", "Vasodilation", "Cardiac output"]
}}
#############################
Example 4:

Query: "What is the role of mitochondria in energy production?"
Answer type pool: {{
'BIOLOGICAL PROCESS': ['CELLULAR RESPIRATION', 'ATP SYNTHESIS'],
'ORGANISM': ['EUKARYOTES', 'HUMAN'],
'MEDICAL CONDITION': ['MITOCHONDRIAL DISEASE', 'OXIDATIVE STRESS'],
'PROTEIN': ['ATP SYNTHASE', 'CYTOCHROME C'],
'GENE': ['MT-ND1', 'MT-COX1'],
'MOLECULE': ['ADENOSINE TRIPHOSPHATE (ATP)', 'OXYGEN'],
'RESEARCH': ['MITOCHONDRIAL STUDIES', 'ENERGY METABOLISM'],
'MEDICAL TREATMENT': ['MITOCHONDRIAL THERAPY', 'ANTIOXIDANT SUPPLEMENTATION'],
'LAB TECHNIQUE': ['MITOCHONDRIAL STAINING', 'OXIDATIVE PHOSPHORYLATION ASSAYS'],
'BEHAVIOR': ['ENERGY METABOLISM', 'AEROBIC RESPIRATION'],
'EMOJI': ['🔋', '🧬'],
'TONE': ['SCIENTIFIC', 'INFORMATIVE'],
'LOCATION': ['CELL BIOLOGY LAB', 'MITOCHONDRIA RESEARCH CENTER']
}}

################
Output:
{{
  "answer_type_keywords": ["BIOLOGICAL PROCESS", "PROTEIN", "MOLECULE"],
  "entities_from_query": ["Mitochondria", "ATP production", "Cellular respiration", "Electron transport chain"]
}}
#############################

-Real Data-
######################
Query: {query}
Answer type pool:{TYPE_POOL}
######################
Output:

"""


PROMPTS[
    "entiti_if_loop_extraction"
] = """It appears some entities may have still been missed.  Answer YES | NO if there are still entities that need to be added.
"""

PROMPTS["fail_response"] = "Sorry, I'm not able to provide an answer to that question."

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to questions about data in the tables provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

{response_type}

---Data tables---

{context_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query.

---Goal---

Given the query, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Output the keywords in JSON format.
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes.
  - "low_level_keywords" for specific entities or details.

######################
-Examples-
######################
Example 1:

Query : "What are the genetic associations between TNFSF4 polymorphisms and systemic sclerosis susceptibility?"
################
Output:
{{
    "high_level_keywords": ["TNFSF4 gene", "Systemic sclerosis", "genetic susceptibility", "Autoimmune disease"],
    "low_level_keywords": ["snp variants", "rs1234314", "rs2205960", "rs844648", "OX40L protein", "Allele frequency"]
}
#############################
Example 2:

Query : "How do TNFSF4 polymorphisms affect different clinical subsets of systemic sclerosis?"
################
Output:
{{
    "high_level_keywords": ["Clinical manifestations", "disease subtypes", "genetic associations", "Autoantibody profiles"],
    "low_level_keywords": ["Limited SSC", "Diffuse SSC", "Anti-centromere antibodies", "Anti-topoisomerase antibodies", "RNA polymerase III antibodies"]
}}
#############################
Example 3:

Query : "What is the role of OX40L in immune regulation and systemic sclerosis pathogenesis?"
################
Output:
{{
    "high_level_keywords": ["Immune regulation", "disease pathogenesis", "T cell responses", "Costimulatory molecules"],
    "low_level_keywords": ["T helper cells", "Regulatory T cells", "Dendritic cells", "Cytokine production", "B cell differentiation", "Antibody production"]
}}
#############################
Example 4:

Query : "How does OX40 and OX40L expression affect atopic dermatitis pathogenesis and progression?"
################
Output: 
{{
    "high_level_keywords": ["OX40", "Atopic dermatitis", "Immune system regulation", "T cell response"],
    "low_level_keywords": ["SOX40", "T cell memory", "Skin inflammation", "Mast cells", "SCORAD index", "Serum levels", "CLA+ T cells"]
}}
#############################
Example 5:

Query: "What is the relationship between OX40 expression and disease severity in atopic dermatitis patients?"
################
Output: 
{{
    "high_level_keywords": ["OX40 expression", "disease severity", "Clinical correlation", "Immunological markers"],
    "low_level_keywords": ["SCORAD correlation", "Serum biomarkers", "T cell populations", "Skin biopsies", "IgE levels", "disease activity"]
}}
#############################
Example 6:

Query: "How do OX40+ and OX40L+ cells interact in atopic dermatitis skin lesions?"
################
Output: 
{{
    "high_level_keywords": ["cell interaction", "Skin pathology", "Immune cell localization", "Inflammatory response"],
    "low_level_keywords": ["cell co-localization", "Dermal expression", "Mast cell markers", "Tryptase staining", "tissue analysis", "Immunofluorescence"]
}}
#############################
-Real Data-
######################
Query: {query}
######################
Output:

"""

PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to questions about documents provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

{response_type}

---Documents---

{content_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""
