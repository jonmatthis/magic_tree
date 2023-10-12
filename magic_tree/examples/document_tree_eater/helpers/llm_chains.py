SUMMARY_PROMPT = """
Summarize the following text, which is a section of an NIH R01. 

The text is writtne in `.tex`. In your summary, you should roughly match the 
structure defined in the `tex` file using markdown heading levels to match tex 
`section` definitions (i.e. # - `section`, ## -`subsection` etc) 
 
 So your summary should look something like this:
 FILE_PATH - [e.g. /document/specific_aims/main_specific_aims.tex]
 STATUS - [an estimate of how close to "done" this is, in a few words] 
 ## [section name]
    ### [subsection name]
        #### [subsubsection name]
 ## [another section name]
 ## Notes:
    - Strengths
        - [list of strengths]
    - Weaknesses
        - [list of weaknesses]
    
 
 DOCUMENT DRAFT TEXT: 
 
 {text}

"""


def create_component_summary_chain():
    prompt = ChatPromptTemplate.from_template(SUMMARY_PROMPT)
    model = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    chain = prompt | model
    return chain


GLOBAL_SUMMARY_PROMPT = """
The following text is an early, incomplete draft of an NIH R01 Proposal

Summarize the main points of the proposal, including the following sections:
# Specific Aims
# Research Strategy
## Significance
## Innovation
## Approach
### Aim 1
### Aim 2

Then list the Strengths and Weaknesses of the proposal

 CURRENT PROPOSAL TEXT: 
 
{text}
"""


def create_global_summary_chain():
    prompt = ChatPromptTemplate.from_template(GLOBAL_SUMMARY_PROMPT)

    model = ChatAnthropic(temperature=0)
    chain = prompt | model
    return chain
