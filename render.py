#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from genXML_h import tewiki, writePage


def getData(row):
    title = str(row['Tel_Heading_2'])
    if len(str(row['Name_Code_Tel'])) > 1:
        title += " - " + str(row['Name_Code_Tel'])
    title += " (" + str(row['Heading']) + ")"
    data = {
        'heading_eng': row['Heading'],
        'heading': str(str(row['Tel_Heading_2']) + "- " + str(row['Name_Code_Tel'])).strip(),
        'category': row['Category_Telugu'],
        'name_code': row['Name_code'],
        'epoch': row['Epoch'],
        'semi_major_axis': round(row['Semi_Major_Axis_AU'], 3),
        'eccentricity': row['Eccentricity'],
        'inclination': row['Inclination_Degrees'],
        'ascending_node_longitude': row['Longitude_of_Ascending_Node_Degrees'],
        'aphelion': round(row['Aphelion_Distance_AU'], 3),
        'perihelion': round(row['Perihelion_Distance_AU'], 3),
        'periapsis_argument': row['Argument_of_Periapsis_Degrees'],
        'mean_anomaly': row['Mean_Anomaly_Degrees'],
        'avg_orbit_speed': round(row['Avg_Orbit_Speed'], 3),
        'orbit_period_days': row['Orbit_Period_Days'],
        'orbit_period_years': round(row['Orbit_Period_Years'], 2),
        'rotation_period': row['Rotation_Period_hours'],
        'diameter': round(row['Diameter_km'], 3),
        'magnitude': row['Magnitude'],
        'is_near_earth': row['Is_Near_Earth_Object'],
        'is_potentially_hazardous': row['Is_Potentially_Hazardous_Object'],
        'size_comparison_object': row['Size_Obj_Telugu'],
        'spectral_type_tholen': row['Spectral_Type_Tholen'],
        'spectral_type_smass': row['Spectral_Type_SMASS'],
	}
    return data

def main():
    file_loader = FileSystemLoader('')
    env = Environment(loader=file_loader, newline_sequence='\n', keep_trailing_newline=True)
    template = env.get_template('asteroid_comet_template.j2')
    
    df = pd.read_csv(open('asteroids_comets_data_v3.csv', 'r'))
    df.fillna('', inplace=True)

    fobj = open('asteroids_articles_edited_all_v4.xml', 'w')
    fobj.write(tewiki+'\n')
    
    count = 0
    for index, row in df.iterrows():
        title = str(row['Tel_Heading_2'])
        if len(str(row['Name_Code_Tel'])) > 1:
            title += " - " + str(row['Name_Code_Tel'])
        title += " (" + str(row['Heading']) + ")"
        text = template.render(getData(row))
        # print(text)
        writePage(title, text, fobj)
        print('\n', index, title)
        count+=1
    

    print(count)
    fobj.write('</mediawiki>')
    fobj.close()


if __name__ == '__main__':
	main()