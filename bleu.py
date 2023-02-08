import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import json

class Analysis_BLEU(object):
    
    def __init__(self, meta_data):
        
        with open(meta_data,'r') as f:
            self.meta_data = json.load(f)
        
    ## reading results (assuming one result per-line with format source_id-target_id-score)
    def read_file(self, file):
        lines = [line.strip().split('-') for line in open(file, encoding = "utf8")]
        for line in lines:
            line[0] = int(line[0])
            line[1] = int(line[1])
            try:
                line[2] = float(line[2])
            except:
                line[2] = -1
        
        dict_types = {}
        for line in lines:
            key = str(self.meta_data['types'][line[0]]) + '-' + str(self.meta_data['types'][line[1]])
            if self.meta_data['pairs'] is None or str(line[0])+'-'+str(line[1]) in self.meta_data['pairs']:
                if line[2] != -1:
                    if key in dict_types:
                        dict_types[key].append(line)
                    else:
                        dict_types[key] = [line]
        return dict_types
                    
    ## reading baseline and model results
    def read_files(self, base_file, model_file):
        
        self.base_dict = self.read_file(base_file)
        self.model_dict = self.read_file(model_file)
        
    ## bucket results for : language pair type, source type, target type
    def diff_bucket_type(self):
        
        sum_base = 0
        sum_prune = 0
        bleu_overal = {}
        for key in self.base_dict.keys():
            len_base = len(self.base_dict[key])
            sum_base = sum([x[2] for x in self.base_dict[key]])/len_base
            sum_prune = sum([x[2] for x in self.model_dict[key]])/len_base
            bleu_overal[key] = (sum_base,sum_prune, (sum_prune-sum_base)/sum_base*100, len_base)
            
        output_overall = {self.meta_data['convert_type'][key.split('-')[0]]+'-to-'+self.meta_data['convert_type'][key.split('-')[1]]: bleu_overal[key][2] for key in bleu_overal }
        
        to_target = {}
        for key in bleu_overal:
            k = key.split('-')[1]
            if k in to_target:
                to_target[k][0] += bleu_overal[key][0]*bleu_overal[key][3]
                to_target[k][1] += bleu_overal[key][1]*bleu_overal[key][3]
                to_target[k][2] += bleu_overal[key][3]
            else:
                to_target[k] = [bleu_overal[key][0]*bleu_overal[key][3],bleu_overal[key][1]*bleu_overal[key][3],bleu_overal[key][3]]

        for key in to_target.keys():
            to_target[key].append((to_target[key][0]/to_target[key][2]))
            to_target[key].append((to_target[key][1]/to_target[key][2]))
            to_target[key].append((to_target[key][1]-to_target[key][0])/to_target[key][0]*100)
    
        output_to_target = {}
        for key in to_target.keys():
            output_to_target["*-to-"+self.meta_data['convert_type'][key]] = to_target[key][-1]
    
    
        to_source = {}
        for key in bleu_overal:
            k = key.split('-')[0]
            if k in to_source:
                to_source[k][0] += bleu_overal[key][0]*bleu_overal[key][3]
                to_source[k][1] += bleu_overal[key][1]*bleu_overal[key][3]
                to_source[k][2] += bleu_overal[key][3]
            else:
                to_source[k] = [bleu_overal[key][0]*bleu_overal[key][3],bleu_overal[key][1]*bleu_overal[key][3],bleu_overal[key][3]]

        for key in to_source.keys():
            to_source[key].append((to_source[key][0]/to_source[key][2]))
            to_source[key].append((to_source[key][1]/to_source[key][2]))
            to_source[key].append((to_source[key][1]-to_source[key][0])/to_source[key][0]*100)

        output_from_source = {}
        for key in to_target.keys():
            output_from_source[self.meta_data['convert_type'][key]+"-to-*"] = to_source[key][-1]
    
        return output_overall, output_to_target, output_from_source
        
    def scatter_plot_diff(self):
        
        scatter_base = {}
        for key in self.base_dict.keys():
            for item in self.base_dict[key]:
                scatter_base[str(item[0])+'-'+str(item[1])] = [min(self.meta_data['bitext'][item[0]],self.meta_data['bitext'][item[1]]),item[2]]
            
        for key in self.model_dict.keys():
            for item in self.model_dict[key]:
                scatter_base[str(item[0])+'-'+str(item[1])].append(item[2])
                diff = (item[2]-scatter_base[str(item[0])+'-'+str(item[1])][-2])
                reldiff = diff/scatter_base[str(item[0])+'-'+str(item[1])][-2]*100
                scatter_base[str(item[0])+'-'+str(item[1])].append(diff)
                scatter_base[str(item[0])+'-'+str(item[1])].append(reldiff)
            
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(25, 40)
        ax = plt.axes()

        x = []
        y = []
        for key in scatter_base.keys():
            x.append(scatter_base[key][0])
            y.append(scatter_base[key][-1])
    
        plt.scatter(x,y,linewidth=10)
        ax.xaxis.grid()
        plt.xticks(fontsize=80)
        plt.yticks(fontsize=80)
        plt.xlabel('Bitext Data for Language Pairs (1M)',fontsize=80)
        plt.ylabel('Relative spBLEU Difference (100%)',fontsize=80)
        
        return scatter_base
