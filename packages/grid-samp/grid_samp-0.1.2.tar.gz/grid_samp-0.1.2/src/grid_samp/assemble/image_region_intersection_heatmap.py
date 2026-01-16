# grid_samp - Grid-based image sampling toolbox
# Copyright (C) 2026 Maarten Leemans, Crhrisophe Bossens, Johan Wagemans
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from PIL import Image
import numpy as np
from matplotlib import cm

class ImageRegionIntersectionHeatmap:
    sigma = 50
    alpha = 0.5
    
    @staticmethod
    def generate(image, Image_Regions):
        intersections = ImageRegionIntersectionHeatmap.get_intersection_points(Image_Regions)
        
        x, y = np.meshgrid(np.arange(0, image.width), np.arange(0, image.height))  # Generates empty values at coordinates x and y
        heatmap = np.zeros_like(x, dtype=float)  # Values set to zero
    
        for intersection in intersections:
            center_x, center_y = intersection
    
            heatmap += np.exp(-((x - center_x) ** 2 + (y - center_y) ** 2) / (2.0 * ImageRegionIntersectionHeatmap.sigma ** 2))
    
        heatmap = heatmap / np.max(heatmap)  # Normalize the heatmap to values between 0 and 1
        cmap = cm.get_cmap('viridis')
        rgba_heatmap = cmap(heatmap)
        rgba_heatmap = (rgba_heatmap[:, :, :3] * 255).astype(np.uint8)
        rgb_heatmap = Image.fromarray(rgba_heatmap, 'RGB')
        # heatmap_img = Image.fromarray(heatmap)  # Convert the heatmap to a Pillow image
        
        blended_img = Image.blend(image.convert('RGBA'), rgb_heatmap.convert('RGBA'), alpha = ImageRegionIntersectionHeatmap.alpha)  # Blend the original image with the heatmap
            
        return blended_img
            
            
    def get_intersection_points(Image_Regions):
        corner_count = {}
        for Image_Region in Image_Regions:
            for corner in Image_Region.get_corners():
                if corner not in corner_count:
                    corner_count[corner] = 1
                else:
                    corner_count[corner] += 1
                
        intersections = []
        for corner in corner_count:
            if corner_count[corner] == 4:
                intersections.append(corner)
                
        return intersections