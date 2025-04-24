import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 设置页面配置
st.set_page_config(
    page_title="House Buying Simulation",
    page_icon="🏠",
    layout="wide"
)

# 初始化会话状态
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
    num_buyers = 5  # 改为5个买家
    
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
    
    # 4. 买家选择模式
    st.write("### Buyer Selection Patterns")
    buyer_patterns = results_df.pivot_table(
        index='buyer', 
        columns='round', 
        values=['price', 'tier', 'type'],
        aggfunc='first'
    ).reset_index()
    
    st.dataframe(buyer_patterns)
    
    # 5. 详细数据表格
    st.write("### Detailed Results")
    st.dataframe(results_df)

# 主界面
def main():
    st.title("House Buying Simulation")
    
    # 模拟说明
    with st.expander("Simulation Instructions", expanded=True):
        st.write("""
        ### Simulation Overview
        - 5 buyers will each complete 3 rounds
        - Each round, buyers will randomly select from 8 available houses
        - Round 1: Limited budget ($100)
        - Round 2-3: Increased budget ($150)
        - Results will show price distribution, tier distribution, and property type distribution
        """)
    
    # 添加模拟按钮
    if st.button("Run Simulation"):
        with st.spinner("Running simulation..."):
            results = run_simulation()
            st.session_state.simulation_results = results
            show_simulation_results(results)
    
    # 如果已经有模拟结果，显示它们
    if st.session_state.simulation_results:
        show_simulation_results(st.session_state.simulation_results)
    
    # 导航到实验页面
    st.sidebar.write("---")
    if st.sidebar.button("Go to Experiment Page"):
        st.switch_page("src/pages/01_Experiment.py")

if __name__ == "__main__":
    main() 