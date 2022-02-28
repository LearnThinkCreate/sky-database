import pandas as pd
import gspread
from .style import HysonStyle
from gspread.exceptions import WorksheetNotFound

def readSpreadsheet(
    sheet_name = None,
    sheet_id = None,
    tab_index = 0,
    ):
    
    gc = gspread.service_account()
    
    if sheet_name:
        gc = gc.open(sheet_name)
    else:
        gc = gc.open_by_key(sheet_id)
    
    values = gc.get_worksheet(tab_index).get_all_values()
    
    df = pd.DataFrame(values)
    df.columns = df.iloc[0]
    df.drop(df.index[0], inplace=True)         

    return df

def updateSpreadsheet(
    df, 
    tab_index = 0, 
    sheet_id = None,
    sheet_name = None,
    tab_name = None,
    styleClass = HysonStyle
    ):
    
    gc = gspread.service_account()
    
    if sheet_name:
        sheet = gc.open(sheet_name)
    else:
        sheet = gc.open_by_key(sheet_id)
    
    try:
        if tab_name:
            worksheet = sheet.worksheet(tab_name)
        else:
            worksheet = sheet.get_worksheet(tab_index)
        # Deleting old values that might cause errors
        worksheet.clear()
        # Updating 
        worksheet.update(([df.columns.values.tolist()] + df.values.tolist()))
    except WorksheetNotFound:
        if tab_name:
            worksheet = sheet.add_worksheet(title=tab_name, cols=len(df.columns), rows=len(df))
        else:
            worksheet = sheet.add_worksheet(cols=len(df.columns), rows=len(df))
        
        # Adding data
        worksheet.update(([df.columns.values.tolist()] + df.values.tolist()))
        # Styling new sheet
        styleClass(worksheet).style()

    return True

def createSpreadsheet(
        df, 
        sheet_name, 
        styleClass = HysonStyle, 
        share_email='whyson@tampaprep.org',
        role='writer',
        perm_type='user'
    ):
    gc = gspread.service_account()
    
    sheet = gc.create(sheet_name)

    # Applying Basic Styling
    worksheet = sheet.sheet1

    sheet.share(share_email, perm_type=perm_type, role=role)
    
    ## Inserting the df
    updateSpreadsheet(df, sheet_id=sheet.id)

    # Applying Basic Styling
    worksheet = sheet.sheet1
    styleClass(worksheet).style()
    return sheet