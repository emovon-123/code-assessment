"""
北京空气质量数据艺术可视化
Beijing Air Quality Data Art Visualization

基于UCI北京多站点空气质量数据集的艺术可视化项目
数据来源：https://archive.ics.uci.edu/ml/datasets/Beijing+Multi-Site+Air-Quality+Data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle
import seaborn as sns
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

class BeijingAirQualityArt:
    def __init__(self, data_path=None):
        """
        初始化北京空气质量艺术可视化器
        
        Args:
            data_path: 数据文件路径，如果为None则生成模拟数据
        """
        self.data_path = data_path
        self.data = None
        self.stations = ['Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 
                        'Guanyuan', 'Gucheng', 'Huairou', 'Nongzhanguan', 
                        'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong']
        
        # 污染物颜色映射
        self.pollutant_colors = {
            'PM2.5': '#FF6B6B',    # 红色 - 细颗粒物
            'PM10': '#4ECDC4',     # 青色 - 可吸入颗粒物
            'SO2': '#45B7D1',      # 蓝色 - 二氧化硫
            'NO2': '#96CEB4',      # 绿色 - 二氧化氮
            'CO': '#FFEAA7',       # 黄色 - 一氧化碳
            'O3': '#DDA0DD'        # 紫色 - 臭氧
        }
        
        # 空气质量等级颜色
        self.aqi_colors = {
            '优': '#00E400',       # 绿色
            '良': '#FFFF00',       # 黄色
            '轻度污染': '#FF7E00',  # 橙色
            '中度污染': '#FF0000',  # 红色
            '重度污染': '#8F3F97',  # 紫色
            '严重污染': '#7E0023'   # 深红色
        }
        
        self.fig, self.ax = plt.subplots(figsize=(16, 12))
        self.setup_plot()
        
    def setup_plot(self):
        """设置绘图区域"""
        self.ax.set_xlim(-2, 10)
        self.ax.set_ylim(-2, 8)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.ax.set_facecolor('#1a1a1a')
        
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
                    'DEWP': temp - 5,  # 露点温度
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
    
    def get_aqi_level(self, pm25):
        """根据PM2.5计算空气质量等级"""
        if pm25 <= 35:
            return '优'
        elif pm25 <= 75:
            return '良'
        elif pm25 <= 115:
            return '轻度污染'
        elif pm25 <= 150:
            return '中度污染'
        elif pm25 <= 250:
            return '重度污染'
        else:
            return '严重污染'
    
    def create_station_layout(self):
        """创建监测站布局"""
        # 模拟北京地图上的监测站位置
        station_positions = {
            'Aotizhongxin': (2, 6),
            'Changping': (1, 7),
            'Dingling': (0.5, 6.5),
            'Dongsi': (4, 5),
            'Guanyuan': (3, 4),
            'Gucheng': (2, 3),
            'Huairou': (1, 5),
            'Nongzhanguan': (5, 4),
            'Shunyi': (6, 6),
            'Tiantan': (4, 3),
            'Wanliu': (3, 2),
            'Wanshouxigong': (2, 1)
        }
        return station_positions
    
    def create_pollutant_visualization(self, frame):
        """创建污染物可视化"""
        self.ax.clear()
        self.setup_plot()
        
        # 获取当前时间的数据
        current_time = self.data['datetime'].iloc[frame % len(self.data['datetime'].unique())]
        current_data = self.data[self.data['datetime'] == current_time]
        
        if current_data.empty:
            return
        
        # 获取监测站位置
        station_positions = self.create_station_layout()
        
        # 绘制监测站
        for _, row in current_data.iterrows():
            station = row['station']
            if station in station_positions:
                x, y = station_positions[station]
                
                # 根据PM2.5浓度确定站点大小和颜色
                pm25 = row['PM2.5']
                aqi_level = self.get_aqi_level(pm25)
                color = self.aqi_colors.get(aqi_level, '#FFFFFF')
                size = max(0.3, min(2.0, pm25 / 100))
                
                # 绘制监测站
                circle = Circle((x, y), size, color=color, alpha=0.8)
                self.ax.add_patch(circle)
                
                # 添加站点标签
                self.ax.text(x, y-0.3, station[:4], ha='center', va='center', 
                           fontsize=8, color='white', weight='bold')
                
                # 添加PM2.5数值
                self.ax.text(x, y+0.3, f'{pm25:.0f}', ha='center', va='center', 
                           fontsize=7, color='white')
        
        # 绘制污染物流动效果
        self.draw_pollutant_flow(current_data, station_positions)
        
        # 添加标题和信息
        title = f"北京空气质量实时监测 - {current_time.strftime('%Y-%m-%d %H:%M')}\n"
        title += f"PM2.5浓度分布 (μg/m³)"
        self.ax.set_title(title, fontsize=16, color='white', pad=20)
        
        # 添加图例
        self.add_legend()
        
        # 添加统计信息
        self.add_statistics(current_data)
    
    def draw_pollutant_flow(self, data, positions):
        """绘制污染物流动效果"""
        # 计算平均风向和风速
        avg_wind_speed = data['WSPM'].mean()
        avg_wind_direction = data['wd'].mean()
        
        if avg_wind_speed > 1:  # 只在有风时绘制流动效果
            # 绘制风向箭头
            center_x, center_y = 5, 4
            wind_x = np.cos(np.radians(avg_wind_direction)) * avg_wind_speed * 0.3
            wind_y = np.sin(np.radians(avg_wind_direction)) * avg_wind_speed * 0.3
            
            self.ax.arrow(center_x, center_y, wind_x, wind_y,
                         head_width=0.2, head_length=0.3,
                         fc='cyan', ec='cyan', alpha=0.7, linewidth=2)
            
            # 添加风向标签
            self.ax.text(center_x + wind_x + 0.5, center_y + wind_y + 0.5,
                        f'风向: {avg_wind_direction:.0f}°\n风速: {avg_wind_speed:.1f}m/s',
                        fontsize=10, color='cyan', weight='bold')
    
    def add_legend(self):
        """添加图例"""
        legend_x = 0.5
        legend_y = 7.5
        
        # 空气质量等级图例
        self.ax.text(legend_x, legend_y, '空气质量等级:', fontsize=12, color='white', weight='bold')
        
        y_offset = 0.3
        for level, color in self.aqi_colors.items():
            circle = Circle((legend_x + 0.5, legend_y - y_offset), 0.1, color=color, alpha=0.8)
            self.ax.add_patch(circle)
            self.ax.text(legend_x + 0.8, legend_y - y_offset, level, fontsize=10, color='white')
            y_offset += 0.25
    
    def add_statistics(self, data):
        """添加统计信息"""
        stats_x = 8
        stats_y = 6
        
        # 计算统计信息
        avg_pm25 = data['PM2.5'].mean()
        max_pm25 = data['PM2.5'].max()
        min_pm25 = data['PM2.5'].min()
        avg_temp = data['TEMP'].mean()
        avg_humidity = data['DEWP'].mean()  # 使用露点温度作为湿度指标
        
        stats_text = f"""实时统计:
平均PM2.5: {avg_pm25:.1f} μg/m³
最高PM2.5: {max_pm25:.1f} μg/m³
最低PM2.5: {min_pm25:.1f} μg/m³
平均温度: {avg_temp:.1f}°C
平均湿度: {avg_humidity:.1f}%"""
        
        self.ax.text(stats_x, stats_y, stats_text, fontsize=10, color='white',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
    
    def start_animation(self, duration=60):
        """启动动画"""
        print("启动北京空气质量艺术可视化...")
        print("按 Ctrl+C 停止动画")
        
        # 加载数据
        self.load_data()
        
        if self.data is None or self.data.empty:
            print("无法加载数据，退出程序")
            return
        
        # 创建动画
        anim = animation.FuncAnimation(self.fig, self.create_pollutant_visualization, 
                                     frames=len(self.data['datetime'].unique()),
                                     interval=200, blit=False, cache_frame_data=False)
        
        # 设置深色主题
        plt.style.use('dark_background')
        
        try:
            plt.show()
        except KeyboardInterrupt:
            print("\n动画已停止")
            plt.close()

def main():
    """主函数"""
    print("=== 北京空气质量数据艺术可视化 ===")
    print("基于UCI北京多站点空气质量数据集")
    print("数据来源: https://archive.ics.uci.edu/ml/datasets/Beijing+Multi-Site+Air-Quality+Data")
    print()
    
    # 创建可视化器
    visualizer = BeijingAirQualityArt()
    
    # 启动动画
    visualizer.start_animation()

if __name__ == "__main__":
    main()
