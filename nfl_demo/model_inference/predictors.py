import pandas as pd
from .utils import *
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib as mpl
from random import random
from statsmodels.sandbox.distributions.extras import pdf_mvsk
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import scipy.stats as stats
import datetime
from copy import deepcopy

class Heirarchical_DM():
    def __init__(self, df, conditions, DV):
        self.df = df
        self.predictor_dict = {}
        self.conditions = conditions
        self.DV = DV
        self.sub_DMs = {}
        self.populate_sub_DMs()

    def populate_sub_DMs(self):
        condition = self.conditions[0]
        uniques = self.df[condition].unique()
        for unique in uniques:
            if len(self.conditions) == 2:
                self.sub_DMs[unique] = Distribution_Manager(self.df[self.df[condition] == unique], self.conditions[1], self.DV)
            else:
                self.sub_DMs[unique] = Heirarchical_DM(self.df[self.df[condition] == unique], self.conditions[1:], self.DV)

    def get_val(self, conditions_vals, percentile):
        if len(conditions_vals) == 2:
            return self.sub_DMs[conditions_vals[0]].get_val(conditions_vals[1], percentile)
        else:
            return self.sub_DMs[conditions_vals[0]].get_val(conditions_vals[1:], percentile)

# ('pos_team', 'pos_winning')
class Distribution_Manager():
    def __init__(self, df, condition, DV):
        self.df = deepcopy(df)
        self.df = self.df.dropna(subset=[DV])
        self.predictor_dict = {}
        self.condition = condition
        self.df_vals = {}
        self.DV = DV
        self.create_vals_dict()

    def create_vals_dict(self):
        uniques = self.df[self.condition].unique()
        uniques.sort()
        for unique in uniques:
            self.df_vals[unique] = self.df[self.df[self.condition] == unique][self.DV].tolist()
            self.df_vals[unique].sort()
            if self.condition is 'run_vs_pass' and False:
                plt.hist(self.df_vals[unique])
                plt.title('cond:' + str(unique) + ', DV:' + self.DV)
                plt.show()

    def get_val(self, condition_val, percentile, count_down_til_no_error=True):
        #print(percentile)
        if percentile > 0.9999999:  # prevents errors due to percentile = 1.0
            percentile = 0.999999
        i = 0
        while True: # galaxy brain tier code
            try:
                return self.df_vals[condition_val][int(percentile * len(self.df_vals[condition_val]))]
            except:
                print('Decaying... condition val =', condition_val)
                condition_val -= 1
                i += 1
                if i > 100:
                    print(condition_val)
                    print('ERROROROROROR')
                    return

class Predictor_Manager():
    def __init__(self, df, formula):
        df_ = deepcopy(df).dropna(subset=[formula.split(' ')[0]]) # drops
        mod = smf.ols(formula=formula, data=df_)
        self.res = mod.fit()
        self.predictions_list = self.res.predict()
        #print('Formula:', formula)
        #print(self.res.summary())
        # print('pre sort:', self.predictions_list)
        # print(vars(self.res.model.data))
        prstd_ols, iv_l_ols, iv_u_ols = wls_prediction_std(self.res, exog=transform_exog_to_model(self.res, df_))
        # print('std:', prstd_ols)
        #print('std:', len(list(prstd_ols)))
        #print('pred:', len(list(self.predictions_list)))

        self.predictions_list = self.predictions_list + np.random.normal(0, 1, prstd_ols.shape[0]) * prstd_ols
        # print('post std:', self.predictions_list)
        self.predictions_list.sort()
        # print('sorted:', self.predictions_list)

    def predict(self, input_df):
        pred_pre_std = self.res.predict(input_df)
        # prstd_ols, iv_l_ols, iv_u_ols = wls_prediction_std(self.res, input_df)
        prstd_ols, iv_l_ols, iv_u_ols = wls_prediction_std(self.res,
                                                           exog=transform_exog_to_model(self.res, input_df))
        z = np.random.normal(0, 1, prstd_ols.shape[0]) * prstd_ols
        pred_final = (pred_pre_std + z).to_numpy()
        # print('std:', prstd_ols)
        # print('pre', pred_pre_std)
        # print('pred:', pred_final)
        pred_indices = np.searchsorted(self.predictions_list, pred_final)
        pred_percentiles = pred_indices / self.predictions_list.shape[0]
        #print('percentiles:', pred_percentiles)
        return pred_percentiles


# from StackOverflow
def transform_exog_to_model(fit, exog):
    transform=True
    self=fit
    # The following is lifted straight from statsmodels.base.model.Results.predict()
    if transform and hasattr(self.model, 'formula') and exog is not None:
        from patsy import dmatrix
        exog = dmatrix(self.model.data.design_info.builder, # removed .orig_exog
                       exog)
    if exog is not None:
        exog = np.asarray(exog)
        if exog.ndim == 1 and (self.model.exog.ndim == 1 or
                               self.model.exog.shape[1] == 1):
            exog = exog[:, None]
        exog = np.atleast_2d(exog)  # needed in count model shape[1]
    return exog

class Basic_Predictor():
    def __init__(self, df, formula, is_custom,co_eff,pos_team,def_team,logistic=False):
        self.df = df
        print(self.df.shape,self.df.columns)
        self.formula = formula
        self.logistic = logistic
        self.res = None
        self.is_custom  = is_custom
        self.co_eff = co_eff
        # if not self.is_custom:
        self.train()
        self.model_coeff = None
        self.pos_team,self.def_team = pos_team,def_team
        
        

    def train(self):
        #print('--')
        #print('formula:', self.formula)
        #print(self.df[['run_vs_pass', 'pos_winning', 'pos_minus_def_score', 'time_left', 'ydstogo']])
        #print('d')
        #print(self.df[['FG_made', 'goal_yd', 'pos_team']])
        if self.logistic:
            self.res = smf.logit(formula=self.formula, data=self.df).fit(disp=0, maxiter=250)
            # print(pd.DataFrame(self.res.params),"yooo model")
            self.model_coeff = pd.DataFrame(self.res.params)

        else:
            self.res = smf.ols(formula=self.formula, data=self.df).fit()
            # print(pd.DataFrame(self.res.params),"yooo model")
            self.model_coeff = pd.DataFrame(self.res.params)

    def predict(self, input_df, get_real_p=False):
        if self.is_custom:
            sum_ = 0
            # print("herererr ",input_df,self.co_eff,self.res)
            for coeff_keys in self.co_eff:
                multiplied_coeff = self.co_eff[coeff_keys]
                mutliplier = 0.75
                new_coeff_keys = coeff_keys.replace("*",":")
                print(new_coeff_keys,self.def_team,self.pos_team,"keys ",self.res.params)
                if new_coeff_keys not in ['pos_team','def_team']:
                    pass
                else:
                    if new_coeff_keys=='pos_team':
                        new_coeff_keys = new_coeff_keys+"[T."+self.pos_team+"]"
                    else:
                        new_coeff_keys = new_coeff_keys+"[T."+self.def_team+"]"
                print(self.res.params.loc[new_coeff_keys],type(self.res.params),"loook at here ")
                self.res.params.loc[new_coeff_keys] = multiplied_coeff*self.res.params.loc[new_coeff_keys]
                print(self.res.params.loc[new_coeff_keys],type(self.res.params),"loook at here aftger that ")


                # print(new_coeff_keys,self.res.params.loc[[new_coeff_keys],['0']],"hetyyyy")

            #     for each_coeff_key in coeff_keys.split("*"):
            #         if each_coeff_key in ['pos_team','def_team']:
            #             # pass
            #             input_df[each_coeff_key].iloc[0] = 1
            #             mutliplier= mutliplier* input_df[each_coeff_key].iloc[0]
            #         else:
            #             # print("waht is this ",input_df[each_coeff_key].iloc[0],mutliplier)
            #             mutliplier= mutliplier* input_df[each_coeff_key].iloc[0]
            #         # print("herere down ",input_df[each_coeff_key].iloc[0],mutliplier)
            #     result = multiplied_coeff*mutliplier
            #     # print(result," sub results",result,multiplied_coeff,mutliplier)
            #     # print("yaayyy model ",pd.DataFrame(self.res.summary().tables[1].data),input_df)
            #     # print(pd.DataFrame(self.res.params),"yooo model",input_df.to_dict())
            #     sum_= sum_ + result
            # # print(sum_,  "         result   ")
            # # print("model ",self.res.__dict__['_results'].__dict__)
            # if self.logistic:
            #     if random() < sum_:
            #         returning = 1
            #     else:
            #         returning = 0
            #     if get_real_p:
            #         return returning, sum_
            #     else:
            #         return returning
            # else:
                
            #     return sum_+np.random.normal(0, 1, 1) * sum_
        # else:
        pred = self.res.predict(input_df)
        if self.logistic:
            if random() < pred[0]: # doesn't work if pred is a np.array or list unlike the linear regression
                returning = 1
            else:
                returning = 0
            if get_real_p:
                return returning, pred[0]
            else:
                return returning
        else:
            prstd_ols, iv_l_ols, iv_u_ols = wls_prediction_std(self.res,
                                                            exog=transform_exog_to_model(self.res, input_df))
            pred = pred + np.random.normal(0, 1, pred.shape[0]) * prstd_ols
            return float(int(pred))