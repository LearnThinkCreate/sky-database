import matplotlib.colors as mcolors
import math

class BaseStyle:
    def __init__(
        self, 
        worksheet
        ):
        self.worksheet = worksheet

    def style(self):
        raise NotImplementedError
        
    def mplColorConverter(self, color, style='backgroundColor'):
        color = mcolors.to_rgb(color)
        return {
            style: {
                'red': math.floor((1- color[0]) * 256),
                'green':math.floor((1- color[1]) * 256),
                'blue': math.floor((1- color[2]) * 256)      
            }
        }

class HysonStyle(BaseStyle):
    def style(self, ncol=100):
        """ Body """
        self.worksheet.format(':', {
                'horizontalAlignment': 'CENTER',
                'textFormat':{
                    'fontSize': 14
                },
            #  'wrapStrategy': 'WRAP',
            })

        """ Header """
        # Bold
        self.worksheet.format('1:', {'textFormat': {'bold': True, 'fontSize':14}})
        # Background color
        self.worksheet.format('1:', self.mplColorConverter(color='lightgrey'))

        self.worksheet.columns_auto_resize(0, ncol)


