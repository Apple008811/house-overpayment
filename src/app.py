import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# 设置页面配置
st.set_page_config(
    page_title="House Buying Experiment",
    page_icon="🏠",
    layout="wide"
)

# 初始化会话状态
if 'current_round' not in st.session_state:
    st.session_state.current_round = 1
if 'budget' not in st.session_state:
    st.session_state.budget = 100
if 'check_opportunities' not in st.session_state:
    st.session_state.check_opportunities = 3
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'viewed_houses' not in st.session_state:
    st.session_state.viewed_houses = set()
if 'purchased_houses' not in st.session_state:
    st.session_state.purchased_houses = []
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = []

# 创建示例房产数据
def create_house_data():
    houses = [
        # Value tier
        {"id": 1, "price": 90, "tier": "Value", "type": "Location", "features": "Basic location"},
        {"id": 2, "price": 100, "tier": "Value", "type": "Property", "features": "Standard features"},
        # Median tier
        {"id": 3, "price": 115, "tier": "Median", "type": "Location", "features": "Commercial area"},
        {"id": 4, "price": 115, "tier": "Median", "type": "Property", "features": "Larger space"},
        {"id": 5, "price": 125, "tier": "Median", "type": "Location", "features": "Business zone"},
        {"id": 6, "price": 125, "tier": "Median", "type": "Property", "features": "Modern amenities"},
        # Premium tier
        {"id": 7, "price": 140, "tier": "Premium", "type": "Location", "features": "School district"},
        {"id": 8, "price": 140, "tier": "Premium", "type": "Property", "features": "Functional backyard"},
        {"id": 9, "price": 150, "tier": "Premium", "type": "Location", "features": "New constructions"},
        {"id": 10, "price": 150, "tier": "Premium", "type": "Property", "features": "Luxury finishes"}
    ]
    return pd.DataFrame(houses)

# 模拟单个买家的决策
def simulate_buyer(round_num, budget):
    houses_df = create_house_data()
    selected_houses = houses_df.sample(n=8)
    
    # 随机选择一个房产
    chosen_house = selected_houses.sample(n=1).iloc[0]
    
    # 检查预算是否足够
    if chosen_house['price'] <= budget:
        return {
            'round': round_num,
            'house_id': chosen_house['id'],
            'price': chosen_house['price'],
            'tier': chosen_house['tier'],
            'type': chosen_house['type']
        }
    else:
        # 如果预算不够，选择最便宜的房产
        affordable_houses = selected_houses[selected_houses['price'] <= budget]
        if not affordable_houses.empty:
            chosen_house = affordable_houses.iloc[0]
            return {
                'round': round_num,
                'house_id': chosen_house['id'],
                'price': chosen_house['price'],
                'tier': chosen_house['tier'],
                'type': chosen_house['type']
            }
        return None

# 运行完整模拟
def run_simulation():
    results = []
    num_buyers = 6
    
    for round_num in range(1, 4):
        # 设置每轮的预算
        budget = 100 if round_num == 1 else 150
        
        for buyer in range(num_buyers):
            result = simulate_buyer(round_num, budget)
            if result:
                result['buyer'] = buyer + 1
                results.append(result)
    
    return pd.DataFrame(results)

# 显示模拟结果
def show_simulation_results(results_df):
    st.write("## Simulation Results")
    
    # 1. 价格分布
    st.write("### Price Distribution by Round")
    fig_price = px.box(results_df, x='round', y='price', 
                      title='Price Distribution by Round')
    st.plotly_chart(fig_price)
    
    # 2. 层级分布
    st.write("### Tier Distribution by Round")
    tier_counts = results_df.groupby(['round', 'tier']).size().unstack(fill_value=0)
    fig_tier = px.bar(tier_counts, title='Tier Distribution by Round',
                     barmode='group')
    st.plotly_chart(fig_tier)
    
    # 3. 类型分布
    st.write("### Property Type Distribution by Round")
    type_counts = results_df.groupby(['round', 'type']).size().unstack(fill_value=0)
    fig_type = px.bar(type_counts, title='Property Type Distribution by Round',
                     barmode='group')
    st.plotly_chart(fig_type)
    
    # 4. 详细数据表格
    st.write("### Detailed Results")
    st.dataframe(results_df)

# 创建房产卡片
def create_house_card(house):
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        st.write(f"**House {house['id']}**")
        st.write(f"Tier: {house['tier']}")
        st.write(f"Type: {house['type']}")
        st.write(f"Features: {house['features']}")
    with col2:
        st.write(f"**Price: ${house['price']}**")
    with col3:
        if st.button(f"View Details", key=f"view_{house['id']}"):
            st.session_state.viewed_houses.add(house['id'])
            st.session_state.current_house = house
        if house['id'] not in st.session_state.viewed_houses:
            if st.button(f"Check Benchmark", key=f"check_{house['id']}"):
                if st.session_state.check_opportunities > 0:
                    st.session_state.check_opportunities -= 1
                    st.session_state.viewed_houses.add(house['id'])
                    st.session_state.current_house = house
                else:
                    st.warning("No more check opportunities remaining!")
        if st.button(f"Purchase", key=f"buy_{house['id']}"):
            if house['price'] <= st.session_state.budget:
                st.session_state.purchased_houses.append(house)
                st.session_state.budget -= house['price']
                st.success(f"Successfully purchased House {house['id']}!")
            else:
                st.error("Insufficient budget!")

# 主界面
def main():
    # 添加模拟按钮
    if st.sidebar.button("Run Simulation"):
        with st.spinner("Running simulation..."):
            results = run_simulation()
            st.session_state.simulation_results = results
            show_simulation_results(results)
    
    # 如果已经有模拟结果，显示它们
    if st.session_state.simulation_results:
        show_simulation_results(st.session_state.simulation_results)
    
    # 原有的实验界面代码...
    # 顶部信息栏
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write(f"**Round:** {st.session_state.current_round}/3")
    with col2:
        remaining_time = 900 - (time.time() - st.session_state.start_time)  # 15 minutes = 900 seconds
        st.write(f"**Time Remaining:** {int(remaining_time//60)}:{int(remaining_time%60):02d}")
    with col3:
        st.write(f"**Budget:** ${st.session_state.budget}")
    with col4:
        st.write(f"**Check Opportunities:** {st.session_state.check_opportunities}/3")

    # 房产展示区
    st.write("## Available Houses")
    
    # 获取并随机选择8个房产
    houses_df = create_house_data()
    selected_houses = houses_df.sample(n=8)
    
    # 创建两列布局
    col1, col2 = st.columns(2)
    
    # 在第一列显示Value和Median tier的房产
    with col1:
        st.write("### Value & Median Tier")
        for _, house in selected_houses[selected_houses['tier'].isin(['Value', 'Median'])].iterrows():
            create_house_card(house)
    
    # 在第二列显示Premium tier的房产
    with col2:
        st.write("### Premium Tier")
        for _, house in selected_houses[selected_houses['tier'] == 'Premium'].iterrows():
            create_house_card(house)

    # 底部状态栏
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Purchased Houses")
        for house in st.session_state.purchased_houses:
            st.write(f"House {house['id']} - ${house['price']}")
    with col2:
        st.write("### Viewed Houses")
        st.write(f"Total viewed: {len(st.session_state.viewed_houses)}")

if __name__ == "__main__":
    main() 