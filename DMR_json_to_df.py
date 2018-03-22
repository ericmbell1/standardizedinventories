#!/usr/bin/env python

import json
import pandas as pd
from pprint import pprint
from pandas.io.json import json_normalize
import os


def main():
    outputdir = set_output_dir('../LCI-Primer-Output/')
    year = '2015'

    drop_list = ['ActualAverageFlowNmbr', 'AllowableLoad', 'AssessmentUnitEPACategory',
                 'AvgConcentration', 'AvgPh', 'AvgPollutantLoad', 'AvgTemp',
                 'AvgWastewaterFlow', 'Cas', 'ChemicalName', 'City',
                 'CongressionalDistNum', 'CountyName', 'CsoCount', 'CwnsIDs', 'DmrYear',
                 'EPARegionCode', 'EffectiveDate', 'ExpirationDate', 'FacilityName',
                 'GeocodeLatitude', 'GeocodeLongitude', 'Huc12', 'Huc12Name',
                 'ImpairedWaterFlg', 'Lc1', 'Lc2', 'Lc3', 'LoadOverLimit1',
                 'LoadOverLimit2', 'Lq1', 'Lq2', 'MajorMinorStatusFlag', 'MaxDailyFlow',
                 'MonitoringLocationCode', 'NdFlag',
                 'PctLoadsDmr', 'PctLoadsLimits', 'PermFeatureNmbr',
                 'PermitTypeCode', 'PollutantDesc',
                 'QcFlag', 'Reachcode', 'SrsID', 'StateWaterBodyName',
                 'TotalDesignFlowNmbr', 'Twf', 'WastewaterFlow', 'Zip']

    file_name = "DMR_" + year + '_standard_format.csv'
    json_data = pd.read_json(path_or_buf='../LCI-Primer-Output/DMR_data.json')
    df = pd.DataFrame(json_data['Results']['Results'])
    df.drop(drop_list, axis=1, inplace=True)

    # Merge reliability table
    # TODO: Determine Reliability criteria?
    reliabilitytable = pd.read_csv('data/DQ_Reliability_Scores_Table3-3fromERGreport.csv',
                                   usecols=['Source', 'Code', 'DQI Reliability Score'])
    dmr_reliabilitytable = reliabilitytable[reliabilitytable['Source'] == 'DMR']
    dmr_reliabilitytable.drop('Source', axis=1, inplace=True)
    df['DQI Reliability Score'] = dmr_reliabilitytable['DQI Reliability Score']

    # Rename with standard column names
    df.rename(columns={'ExternalPermitNmbr': 'FacilityID'}, inplace=True)
    df.rename(columns={'Siccode': 'SIC'}, inplace=True)
    df.rename(columns={'StateCode': 'State'}, inplace=True)
    df.rename(columns={'ParameterDesc': 'OriginalFlowID'}, inplace=True)
    df.rename(columns={'DQI Reliability Score': 'ReliabilityScore'}, inplace=True)
    df.rename(columns={'PollutantLoad': 'Amount'}, inplace=True)
    df = df[df['Amount'] != '--']
    # Already in kg/yr, so no conversion necessary

    df.drop(['EstFactor', 'TRIDirectPounds', 'TRIIndirectPounds'], axis=1, inplace=True)
    df.to_csv(path_or_buf=outputdir + file_name, index=False)




# sets the output directory
def set_output_dir(directory):
    outputdir = directory
    if not os.path.exists(outputdir): os.makedirs(outputdir)
    return outputdir


if __name__ == '__main__':
    main()
