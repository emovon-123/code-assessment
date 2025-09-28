"""
康定斯基风格空气质量抽象艺术
Kandinsky-Style Air Quality Abstract Art

将空气质量数据转换为康定斯基风格的抽象几何图形和线条变化
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle, Polygon, Wedge
import seaborn as sns
from datetime import datetime, timedelta
import os
import warnings
import random
import math
warnings.filterwarnings('ignore')

class KandinskyAirArt:
    def __init__(self, data_path=None):
        """初始化康定斯基风格空气质量抽象艺术生成器"""
        self.data_path = data_path
        self.data = None
        self.stations = ['Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 
                        'Guanyuan', 'Gucheng', 'Huairou', 'Nongzhanguan', 
                        'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong']
        
        # 康定斯基风格颜色调色板
        self.kandinsky_colors = {
            'primary': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'],
            'secondary': ['#FF8E53', '#6C5CE7', '#A29BFE', '#FD79A8', '#FDCB6E', '#6C5CE7'],
            'accent': ['#E17055', '#00B894', '#0984E3', '#00CEC9', '#FDCB6E', '#E84393'],
            'neutral': ['#2D3436', '#636E72', '#74B9FF', '#81ECEC', '#FAB1A0', '#FF7675']
        }
        
        # 抽象图形元素
        self.abstract_shapes = []
        self.abstract_lines = []
        self.abstract_circles = []
        self.abstract_triangles = []
        self.abstract_rectangles = []
        
        self.fig, self.ax = plt.subplots(figsize=(16, 12))
        self.setup_plot()
        
    def setup_plot(self):
        """设置绘图区域"""
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.ax.set_facecolor('#e5dbc3')  # 米色背景
        
    def generate_mock_data(self, days=30):
        """生成模拟的北京空气质量数据"""
        print("生成模拟北京空气质量数据...")
        
        # 生成时间序列
        start_date = datetime(2023, 1, 1)
        dates = [start_date + timedelta(hours=i) for i in range(days * 24)]
        
        data = []
        for i, date in enumerate(dates):
            # 模拟季节性变化
            seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * i / (365 * 24))
            
            # 模拟日变化
            daily_factor = 1 + 0.5 * np.sin(2 * np.pi * (i % 24) / 24)
            
            # 模拟随机波动
            random_factor = np.random.normal(1, 0.2)
            
            for station in self.stations:
                # 不同站点有不同的基础污染水平
                station_factor = np.random.uniform(0.8, 1.2)
                
                # 生成污染物数据
                pm25 = max(0, 50 * seasonal_factor * daily_factor * random_factor * station_factor)
                pm10 = pm25 * np.random.uniform(1.2, 1.8)
                so2 = max(0, 20 * seasonal_factor * random_factor * station_factor)
                no2 = max(0, 40 * seasonal_factor * daily_factor * random_factor * station_factor)
                co = max(0, 2 * seasonal_factor * daily_factor * random_factor * station_factor)
                o3 = max(0, 80 * seasonal_factor * daily_factor * random_factor * station_factor)
                
                # 气象数据
                temp = 15 + 20 * np.sin(2 * np.pi * i / (365 * 24)) + np.random.normal(0, 5)
                pressure = 1013 + np.random.normal(0, 10)
                humidity = max(0, min(100, 60 + 20 * np.sin(2 * np.pi * i / (365 * 24)) + np.random.normal(0, 15)))
                wind_speed = max(0, 3 + np.random.exponential(2))
                wind_direction = np.random.uniform(0, 360)
                
                data.append({
                    'datetime': date,
                    'station': station,
                    'PM2.5': pm25,
                    'PM10': pm10,
                    'SO2': so2,
                    'NO2': no2,
                    'CO': co,
                    'O3': o3,
                    'TEMP': temp,
                    'PRES': pressure,
                    'DEWP': temp - 5,
                    'RAIN': max(0, np.random.exponential(0.5)),
                    'WSPM': wind_speed,
                    'wd': wind_direction
                })
        
        self.data = pd.DataFrame(data)
        print(f"生成了 {len(self.data)} 条记录，涵盖 {len(self.stations)} 个监测站")
        return self.data
    
    def load_data(self):
        """加载数据"""
        if self.data_path and os.path.exists(self.data_path):
            try:
                print(f"加载数据文件: {self.data_path}")
                self.data = pd.read_csv(self.data_path)
                print(f"成功加载 {len(self.data)} 条记录")
            except Exception as e:
                print(f"加载数据文件失败: {e}")
                print("使用模拟数据...")
                self.generate_mock_data()
        else:
            print("未找到数据文件，使用模拟数据...")
            self.generate_mock_data()
    
    def get_kandinsky_color(self, value, color_type='primary'):
        """根据数值获取康定斯基风格颜色"""
        colors = self.kandinsky_colors[color_type]
        
        # 将数值映射到颜色索引
        if value < 50:
            return colors[0]  # 红色系
        elif value < 100:
            return colors[1]  # 青色系
        elif value < 150:
            return colors[2]  # 蓝色系
        elif value < 200:
            return colors[3]  # 绿色系
        elif value < 250:
            return colors[4]  # 黄色系
        else:
            return colors[5]  # 紫色系
    
    def create_abstract_circles(self, data):
        """创建抽象圆形元素"""
        circles = []
        
        for _, row in data.iterrows():
            # 根据PM2.5浓度创建圆形
            pm25 = row['PM2.5']
            size = max(0.5, min(3.0, pm25 / 50))
            color = self.get_kandinsky_color(pm25, 'primary')
            
            # 随机位置
            x = random.uniform(-8, 8)
            y = random.uniform(-8, 8)
            
            # 根据风向调整位置
            wind_direction = row['wd']
            wind_x = np.cos(np.radians(wind_direction)) * 0.5
            wind_y = np.sin(np.radians(wind_direction)) * 0.5
            
            circle = {
                'x': x + wind_x,
                'y': y + wind_y,
                'radius': size,
                'color': color,
                'alpha': random.uniform(0.4, 0.8),
                'rotation': random.uniform(0, 360)
            }
            circles.append(circle)
        
        return circles
    
    def create_abstract_triangles(self, data):
        """创建抽象三角形元素"""
        triangles = []
        
        for _, row in data.iterrows():
            # 根据SO2浓度创建三角形
            so2 = row['SO2']
            size = max(0.3, min(2.0, so2 / 30))
            color = self.get_kandinsky_color(so2, 'secondary')
            
            # 随机位置
            x = random.uniform(-7, 7)
            y = random.uniform(-7, 7)
            
            # 根据温度调整三角形大小
            temp = row['TEMP']
            temp_factor = (temp + 20) / 40  # 标准化温度
            
            triangle = {
                'x': x,
                'y': y,
                'size': size * temp_factor,
                'color': color,
                'alpha': random.uniform(0.3, 0.7),
                'rotation': random.uniform(0, 360)
            }
            triangles.append(triangle)
        
        return triangles
    
    def create_abstract_rectangles(self, data):
        """创建抽象矩形元素"""
        rectangles = []
        
        for _, row in data.iterrows():
            # 根据NO2浓度创建矩形
            no2 = row['NO2']
            width = max(0.2, min(1.5, no2 / 40))
            height = max(0.2, min(1.5, no2 / 40))
            color = self.get_kandinsky_color(no2, 'accent')
            
            # 随机位置
            x = random.uniform(-6, 6)
            y = random.uniform(-6, 6)
            
            # 根据湿度调整矩形透明度
            humidity = row['DEWP']
            alpha = max(0.2, min(0.8, humidity / 100))
            
            rectangle = {
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'color': color,
                'alpha': alpha,
                'rotation': random.uniform(0, 360)
            }
            rectangles.append(rectangle)
        
        return rectangles
    
    def create_abstract_lines(self, data):
        """创建抽象线条元素"""
        lines = []
        
        for _, row in data.iterrows():
            # 根据风速创建线条
            wind_speed = row['WSPM']
            wind_direction = row['wd']
            
            if wind_speed > 2:  # 只在有风时创建线条
                # 线条长度与风速相关
                length = max(1.0, min(4.0, wind_speed / 2))
                
                # 起始点
                start_x = random.uniform(-8, 8)
                start_y = random.uniform(-8, 8)
                
                # 根据风向计算终点
                end_x = start_x + np.cos(np.radians(wind_direction)) * length
                end_y = start_y + np.sin(np.radians(wind_direction)) * length
                
                # 根据CO浓度选择颜色
                co = row['CO']
                color = self.get_kandinsky_color(co, 'neutral')
                
                line = {
                    'start_x': start_x,
                    'start_y': start_y,
                    'end_x': end_x,
                    'end_y': end_y,
                    'color': color,
                    'width': max(1, min(5, wind_speed)),
                    'alpha': random.uniform(0.4, 0.8)
                }
                lines.append(line)
        
        return lines
    
    def create_abstract_polygons(self, data):
        """创建抽象多边形元素"""
        polygons = []
        
        for _, row in data.iterrows():
            # 根据O3浓度创建多边形
            o3 = row['O3']
            if o3 > 50:  # 只在O3浓度较高时创建
                sides = random.randint(5, 8)
                size = max(0.5, min(2.0, o3 / 100))
                color = self.get_kandinsky_color(o3, 'primary')
                
                # 随机位置
                center_x = random.uniform(-7, 7)
                center_y = random.uniform(-7, 7)
                
                # 生成多边形顶点
                vertices = []
                for i in range(sides):
                    angle = 2 * np.pi * i / sides
                    x = center_x + size * np.cos(angle)
                    y = center_y + size * np.sin(angle)
                    vertices.append([x, y])
                
                polygon = {
                    'vertices': vertices,
                    'color': color,
                    'alpha': random.uniform(0.3, 0.6),
                    'rotation': random.uniform(0, 360)
                }
                polygons.append(polygon)
        
        return polygons
    
    def draw_abstract_circles(self, circles):
        """绘制抽象圆形"""
        for circle in circles:
            # 绘制主圆形
            main_circle = Circle((circle['x'], circle['y']), circle['radius'], 
                               color=circle['color'], alpha=circle['alpha'])
            self.ax.add_patch(main_circle)
            
            # 绘制内圆
            inner_circle = Circle((circle['x'], circle['y']), circle['radius'] * 0.6, 
                                color='white', alpha=0.3)
            self.ax.add_patch(inner_circle)
            
            # 绘制外圆
            outer_circle = Circle((circle['x'], circle['y']), circle['radius'] * 1.3, 
                                color=circle['color'], alpha=0.2)
            self.ax.add_patch(outer_circle)
    
    def draw_abstract_triangles(self, triangles):
        """绘制抽象三角形"""
        for triangle in triangles:
            # 计算三角形顶点
            x, y = triangle['x'], triangle['y']
            size = triangle['size']
            
            # 等边三角形顶点
            vertices = [
                [x, y + size],
                [x - size * 0.866, y - size * 0.5],
                [x + size * 0.866, y - size * 0.5]
            ]
            
            # 旋转三角形
            angle = np.radians(triangle['rotation'])
            rotated_vertices = []
            for vx, vy in vertices:
                rx = (vx - x) * np.cos(angle) - (vy - y) * np.sin(angle) + x
                ry = (vx - x) * np.sin(angle) + (vy - y) * np.cos(angle) + y
                rotated_vertices.append([rx, ry])
            
            polygon = Polygon(rotated_vertices, color=triangle['color'], 
                            alpha=triangle['alpha'])
            self.ax.add_patch(polygon)
    
    def draw_abstract_rectangles(self, rectangles):
        """绘制抽象矩形"""
        for rectangle in rectangles:
            # 计算矩形顶点
            x, y = rectangle['x'], rectangle['y']
            w, h = rectangle['width'], rectangle['height']
            
            # 矩形顶点
            vertices = [
                [x - w/2, y - h/2],
                [x + w/2, y - h/2],
                [x + w/2, y + h/2],
                [x - w/2, y + h/2]
            ]
            
            # 旋转矩形
            angle = np.radians(rectangle['rotation'])
            rotated_vertices = []
            for vx, vy in vertices:
                rx = (vx - x) * np.cos(angle) - (vy - y) * np.sin(angle) + x
                ry = (vx - x) * np.sin(angle) + (vy - y) * np.cos(angle) + y
                rotated_vertices.append([rx, ry])
            
            polygon = Polygon(rotated_vertices, color=rectangle['color'], 
                            alpha=rectangle['alpha'])
            self.ax.add_patch(polygon)
    
    def draw_abstract_lines(self, lines):
        """绘制抽象线条"""
        for line in lines:
            self.ax.plot([line['start_x'], line['end_x']], 
                        [line['start_y'], line['end_y']],
                        color=line['color'], linewidth=line['width'], 
                        alpha=line['alpha'])
    
    def draw_abstract_polygons(self, polygons):
        """绘制抽象多边形"""
        for polygon in polygons:
            # 旋转多边形
            angle = np.radians(polygon['rotation'])
            center_x = sum(v[0] for v in polygon['vertices']) / len(polygon['vertices'])
            center_y = sum(v[1] for v in polygon['vertices']) / len(polygon['vertices'])
            
            rotated_vertices = []
            for vx, vy in polygon['vertices']:
                rx = (vx - center_x) * np.cos(angle) - (vy - center_y) * np.sin(angle) + center_x
                ry = (vx - center_x) * np.sin(angle) + (vy - center_y) * np.cos(angle) + center_y
                rotated_vertices.append([rx, ry])
            
            polygon_patch = Polygon(rotated_vertices, color=polygon['color'], 
                                  alpha=polygon['alpha'])
            self.ax.add_patch(polygon_patch)
    
    def create_abstract_visualization(self, frame):
        """创建抽象可视化"""
        self.ax.clear()
        self.setup_plot()
        
        # 获取当前时间的数据
        current_time = self.data['datetime'].iloc[frame % len(self.data['datetime'].unique())]
        current_data = self.data[self.data['datetime'] == current_time]
        
        if current_data.empty:
            return
        
        # 创建抽象元素
        circles = self.create_abstract_circles(current_data)
        triangles = self.create_abstract_triangles(current_data)
        rectangles = self.create_abstract_rectangles(current_data)
        lines = self.create_abstract_lines(current_data)
        polygons = self.create_abstract_polygons(current_data)
        
        # 绘制抽象元素
        self.draw_abstract_circles(circles)
        self.draw_abstract_triangles(triangles)
        self.draw_abstract_rectangles(rectangles)
        self.draw_abstract_lines(lines)
        self.draw_abstract_polygons(polygons)
        
        # 添加背景渐变效果
        self.add_background_gradient(current_data)
    
    def add_background_gradient(self, data):
        """添加背景渐变效果"""
        # 根据平均PM2.5浓度调整背景
        avg_pm25 = data['PM2.5'].mean()
        
        if avg_pm25 < 50:
            bg_color = '#e5dbc3'  # 基础米色
        elif avg_pm25 < 100:
            bg_color = '#d4c5a0'  # 稍深米色
        elif avg_pm25 < 150:
            bg_color = '#c3b07d'  # 更深米色
        else:
            bg_color = '#b29b5a'  # 最深米色
        
        self.ax.set_facecolor(bg_color)
    
    def start_animation(self, duration=60):
        """启动动画"""
        print("启动康定斯基风格空气质量抽象艺术...")
        print("按 Ctrl+C 停止动画")
        
        # 加载数据
        self.load_data()
        
        if self.data is None or self.data.empty:
            print("无法加载数据，退出程序")
            return
        
        # 创建动画
        anim = animation.FuncAnimation(self.fig, self.create_abstract_visualization, 
                                     frames=len(self.data['datetime'].unique()),
                                     interval=1000, blit=False, cache_frame_data=False)
        
        # 设置深色主题
        plt.style.use('dark_background')
        
        try:
            plt.show()
        except KeyboardInterrupt:
            print("\n动画已停止")
            plt.close()

def main():
    """主函数"""
    print("=== 康定斯基风格空气质量抽象艺术 ===")
    print("将空气质量数据转换为抽象几何图形和线条变化")
    print()
    
    # 创建抽象艺术生成器
    artist = KandinskyAirArt()
    
    # 启动动画
    artist.start_animation()

if __name__ == "__main__":
    main()
