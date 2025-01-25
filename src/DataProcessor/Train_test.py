import pandas as pd

from Utils.IO.JSON_File_IO import load_JSON_to_Dataframe, save_Dataframe_to_JSON

data_json_file = 'D:\Research\Data\Intelligent_Feedback\RQ1\Llama_ZERO_signature.json'
# Load the dataframe
df = load_JSON_to_Dataframe(data_json_file)

# drop  "es_results" column
# df.drop(columns=['es_results'], inplace=True)




# group the dataframe by project and sub_project
grouped_df = df.groupby(['project', 'sub_project'])

# sort them by bug_id and split 80:20 for train and test

train_df = pd.DataFrame()
test_df = pd.DataFrame()


project_stat = {}

for name, group in grouped_df:
    group = group.sort_values(by='bug_id')
    train_group = group[:int(0.8 * len(group))]
    test_group = group[int(0.8 * len(group)):]

    # print project name and the number of bugs in the project
    # print('Project:', name, len(group), 'Train:', len(train_group), 'Test:', len(test_group))

    # check project exists in the project_stat. if not add it, else increment the count
    if name[0] not in project_stat:
        project_stat[name[0]] = {'total': len(group), 'train': len(train_group), 'test': len(test_group)}
    else:
        project_stat[name[0]]['total'] += len(group)
        project_stat[name[0]]['train'] += len(train_group)
        project_stat[name[0]]['test'] += len(test_group)

    train_df = pd.concat([train_df, train_group])
    test_df = pd.concat([test_df, test_group])

# print the project statistics
for key, value in project_stat.items():
    print('Project:', key, 'Total:', value['total'], 'Train:', value['train'], 'Test:', value['test'])

print('Total Train', len(train_df))
print('Total Test', len(test_df))




# Save the train and test dataframes
# save_Dataframe_to_JSON(train_df, 'D:\Research\Data\Intelligent_Feedback\\train_test\\train.json')
save_Dataframe_to_JSON(test_df, 'D:\Research\Data\Intelligent_Feedback\\train_test\\test-Llama.json')