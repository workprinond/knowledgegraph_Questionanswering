# formates a JSON to a dataframe
def dataframe_formatter(entry, vars):
    res = {}
    for key in vars:
        res[key] = entry[key]['value']
    return res


# generic string splitter
def string_extractor(string, splitter): return string.split(splitter)[-1]

# generic string replace for multiple characters
def string_replace(ls, string):
    for l in ls:
        string = string.replace(l, '')
    return string

# applys our string splitter fn to given cols of a dataframe
def dataFrame_extractor(df, cols, splitter):
    for col in cols:
        df[col] = df[col].apply(lambda x: string_extractor(x, splitter))
    return df


## formates the returning comment
def comment_formatter(comment, index):
    split = comment.split()[index:]
    return ' '.join(split)


def formate_name(name):
    if name == 'Alzheimer disease':
        return 'Alzheimer\'s Disease'
    else: 
        if name == 'anxiety':
            return name.capitalize()
    # else: 
    #     if name == 'glaucoma':
    #         return name.capitalize()
        
    return name

def definition_name_formatter(name):
    if name == 'Alzheimer disease':
        name = 'alzheimer\'s disease'
    return name


## printer function for the definition intent
def definition_printer(df, name):
    answers = []
    for row in df.iterrows():
        answers.append(
            'The disease ' +
            name.upper() +
            ' with DOID: ' + row[1]['doid'] +
            ' has the  UML, short for Unified Modeling Language, ' + row[1]['umlsTerm'].upper() +
            ' , and UMLs ID: ' + row[1]['umls']
        )
    return answers



def casuation_printer(df, name):
    answers = ['These are the top genes associated with ' + name]

    if len(df) > 2:
        
        answers.append(
            '\n' +
            'The first one has the Gene ID: ' + df.loc[[0]]['gene'][0]
            + ' , its medically known as: ' + df.loc[[0]]['name'][0].upper()
            + ' , and it has association score equal to ' + df.loc[[0]]['score'][0]
            + '\n'
            + ' , and the second has the ID: ' + df.loc[[1]]['gene'][1]
            + ' , its medically known as: ' + df.loc[[1]]['name'][1].upper()
            + ' , and it has association score equal to ' + df.loc[[1]]['score'][1]
        )
    else:
        answers.append(
            '\n' +
            'The Gene has the Gene ID: ' + df.loc[[0]]['gene'][0]
            + ' , its medically known as: ' + df.loc[[0]]['name'][0].upper()
            + ' , and it has association score equal to ' + df.loc[[0]]['score'][0]
        )

    return ' '.join(answers)
    
def association_printer(df, name):
    answers = ['The disease ' + name]
    for row in df.iterrows():
        answers.append(
            '\n' +
            ' and the Gene ' + row[1]['gene'] +
            ' have an association score of ' + row[1]['score'] +
            ' and association type of ' + row[1]['associationType'] +
            '\n' +
            ' I have  retrieved the supporting evidences  ' + string_replace(['[', ']'], row[1]['sentence'])
        )
    return ' '.join(answers)