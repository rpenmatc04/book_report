import os
import openai


# Independent chunk based analysis 
def LiteraryAnalyst(excerpt, modelName, client):

  system = "You are a Literary Analyst focused on the theme of social isolation. Identify multiple passages, quotes, and examples that display this theme in the excerpt."

  prompt = f"Analyze the following excerpt, specifically about the theme of social isolation. Return direct quotes and examples from the text, and explain how they relate to social isolation: \n {excerpt}"

  completion = client.chat.completions.create(
    model = modelName,
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": prompt}
    ]
  )
  
  return completion.choices[0].message.content

# Dependent chunk based analysis
def LiteraryAnalystIncremental(pastResponses, excerpt, modelName, client):
  pastResponses = '\n'.join(pastResponses)
  
  system = "You are a Literary Analyst focused on the theme of social isolation. Identify multiple passages, quotes, and examples that display this theme in the excerpt."

  prompt = f"Below are analyses of previous sections of the text regarding the theme of social isolation:\n\n{pastResponses}\n\nNow, analyze the following excerpt in the context of these past responses. Identify direct quotes and examples that display social isolation, and explain how they connect to or expand upon the theme as established in prior sections:\n\n{excerpt}"

  completion = client.chat.completions.create(
    model = modelName,
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": prompt}
    ]
  )
  
  return completion.choices[0].message.content

# Analyzing all the chunks in a text to combine it into one 
def SummarizeNovelLevelAnalysis(chunks, modelName, client):  
  analyses = '\n'.join(chunks)

  system = "You are a Literary Analyst focused on synthesizing analysis about social isolation. Your goal is to return a novel-level summary about how this work " \
  "displays the theme of social isolation. Reference the most important quotes, examples, and passages in the chunk-level analyses, and explain their significance."

  prompt = f"Below are chunk-level analyses produced for the novel. Please synthesize these into a single, detailed summary focused on the theme of social isolation. Return important quotes and explanations that highlight the author's perspective on social isolation. If the chunk analyses do not contain a particular detail or example, do not make it up. Generate the summary only on the chunk-level analyses provided below: \n {analyses}"
  
  completion = client.chat.completions.create(
    model = modelName,
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": prompt}
    ]
  )
  
  return completion.choices[0].message.content

# Analyzing two chunks in a text to combine it into one (hierarchical merging)
def SummarizeNovelLevelAnalysisHierarchical(chunk_1, chunk_2, modelName, client):  

  system = "You are a Literary Analyst focused on synthesizing analysis about social isolation. Your goal is to return a summary about how this work " \
  "displays the theme of social isolation. Reference the most important quotes, examples, and passages in the chunk-level analyses, and explain their significance."

  prompt = f"Below are two chunk-level analyses produced for the novel. Please synthesize these into a single, detailed summary focused on the theme of social isolation. Return important quotes and explanations that highlight the author's perspective on social isolation. If the chunk analyses do not contain a particular detail or example, do not make it up. Generate the summary only on the chunk-level analyses provided below: \n {chunk_1} \n {chunk_2}"
  
  completion = client.chat.completions.create(
    model = modelName,
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": prompt}
    ]
  )
  
  return completion.choices[0].message.content

# Comparative Analysis given results of either of the two previous Summary calls
def CompareBooks(novels, modelName, client):
  compare_analyses = '\n'.join(novels)

  system = "You are an expert at comparing literature. Create a detailed comparison of how different novels approach the theme of social isolation, focusing on the author's point of view, as well as supporting quotations, passages, and corresponding explanations."
  
  prompt = f"Compare and contrast how these following novels handle the theme of social isolation. The following are analyses of how each novel handles the theme. Identify how each text handles the theme of social isolation and how they differ approach, perspective, and resolution of this theme by including several specific examples. If the novel analyses do not contain a particular detail or example, do not make it up. Generate the summary only using analyses provided below: \n {compare_analyses}"


  completion = client.chat.completions.create(
    model = modelName,
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": prompt}
    ]
  )
  
  return completion.choices[0].message.content


# Singular Call to Generate Report 
def GenerateReport(comparison, modelName, client):
  system = "You are an expert book report writer with a focus on comparative literary analysis. Your task is to create a detailed book report analyzing how different books explore the theme of social isolation by providing detailed comparisons, highlighting themes, and discussing the techniques and views of the authors."
  
  prompt = f"""
  Write a five-paragraph comparative book report based on a Comparative Analysis to explain how the works handle the theme of social isolation."

  Structure of Report: 
  Introduction Paragraph: Introduce the books and end with a strong thesis statement about how each book deals with social isolation
  First Body Paragraph: Explain how the first book deals with the topic of social isolation with at least 1-2 direct references to the text.
  Second Body Paragraph: Explain how the second book deals with the topic of social isolation with at least 1-2 direct references to the text.
  Third Body Paragraph: Explain how the third book deals with the topic of social isolation with at least 1-2 direct references to the text.
  Conclusion Paragraph: Summarize the key points in the body paragraphs as well as restating the thesis. 

  Requirements: 
  Each body paragraph must include direct and accurate quotations from the book. 
  The report should focus on the differences and similarities in how each author views and expresses the theme of social isolation.
  The report should be in a professional tone and digestible.

  The Comparative Analysis is included below: \n {comparison}
  """


  completion = client.chat.completions.create(
    model = modelName,
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": prompt}
    ]
  )
  
  return completion.choices[0].message.content

def GenerateBodyParagraphs(comparison, modelName, client):

    system = "You are an expert in literary comparison. Your goal is to write three body paragraphs that each focus solely on how one of the three books addresses the theme of social isolation. " \
    "Each paragraph must include at least one to two direct quotes or passages from the provided analysis only if available."

    prompt = f"""
        Below is a comparative analysis of three novels' approaches to social isolation. 
        Using only this analysis, write three body paragraphs:
        Body Paragraph 1: Focus on the first book, analyzing how it treats social isolation with supporting quotes.
        Body Paragraph 2: Focus on the second book, analyzing how it treats social isolation with supporting quotes.
        Body Paragraph 3: Focus on the third book, analyzing how it treats social isolation with supporting quotes.
        Each paragraph should focus on one novel's themes and views, with direct quotes only if available.
        Comparative Analysis: \n{comparison}
    """

    completion = client.chat.completions.create(
        model=modelName,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content

def GenerateIntroduction(body_paragraphs, comparison, modelName, client):

    system = "You are an expert in literary comparison. Your goal is to write an introduction paragraph with a strong thesis for a comparative book report on " \
    "social isolation across three works. The introduction must reference the already written body paragraphs."

    prompt = f"""
        Below is the following body paragraphs already written: \n
        {body_paragraphs} \n \n 
        Below is the comparative analysis of the three novels for additional context: \n
        {comparison} \n \n
        Write a single introduction paragraph with the following goals: \n
        1. Clear thesis of how the theme of social isolation is handled in the three books by referencing the analysis in the body paragraphs, 
        2. Mention the title of the three books and the authors.
        3. Describe the main points to be detailed in the body paragraphs.
    """

    completion = client.chat.completions.create(
        model=modelName,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content

def GenerateConclusion(introduction, body_paragraphs, comparison, modelName, client):

    system =  f"""You are a literary analyst. Your goal is to write a single conclusion paragraph with the following goals: \n 
        1. Synthesize the key similarities and differences among the three novels regarding the theme of social isolation
        2. Restate the thesis in a different way, and 
        3. Final thought on social isolation."""

    prompt = f"""
        Below is the introduction already written: \n
        {introduction} \n \n 
        Below is the three body paragraphs: \n
        {body_paragraphs} \n \n
        Finally, here is the generated comparative analysis for the three texts for extra reference: \n
        {comparison} \n \n
        Write a single conclusion paragraph with the following goals: \n
        1. Summarize the main points about similarities and differences from the body paragraphs
        2. Restate the thesis in a different way  
        3. Leave a final thought on why these comparisons matter and about social isolation.
    """

    completion = client.chat.completions.create(
        model=modelName,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content


def CompareBookReports(report1, report2, modelName, client):
  system = """ 
      You are an expert literary analyst. Compare two book reports based on the following three factors: 
      the depth of analysis and evidence, writing clarity, and logical coherence. 
      Evaluate both reports carefully."
      Return only '0' if the first is better or '1' if the second is better. 
      """

  prompt = f"""
      Here are two book reports analyzing how the same books explore the theme of social isolation. 
      Evaluate them independently based on depth of analysis, writing clarity, and logical coherence. 
      After considering both carefully, determine which one is stronger overall. 
      Provide your answer as '0' if Report 1 is better or '1' if Report 2 is better. 
      The positions are irrelevant .\n\n
      Book Report 1:\n {report1} \n\n Book Report 2:\n {report2}.
      """

  print(prompt)
  completion = client.chat.completions.create(
      model=modelName,
      messages=[
          {"role": "system", "content": system},
          {"role": "user", "content": prompt}
      ]
  )

  return completion.choices[0].message.content


# Useful for Testing 
def get_best_output(outputs, modelName, client): 
    while len(outputs) > 1:
         # Comparison Based Judger on Two Reports until One is Left
        temp = CompareBookReports(outputs[0], outputs[1], modelName, client)
        saved = outputs[0]
        if '0' in temp[0:5]:
            saved = outputs[0]
        elif '1' in temp[0:5]: 
            saved = outputs[1]
        else: 
            print("Error")
 
        outputs = outputs[2:]
        outputs.append(saved)