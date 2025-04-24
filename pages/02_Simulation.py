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
        {"id": 8, "price": 140, "tier": "Premium", "type": "Property", "features": "Functional backyard"}
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
    num_buyers = 5  # 5个买家
    
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

    # 新增：买家行为分析部分
    st.write("## Buyer Behavior Analysis")
    
    with st.expander("Buyer Behavior Analysis", expanded=True):
        # 1. 买家预算使用率
        st.write("### Budget Utilization")
        budget_utilization = results_df.groupby(['buyer', 'round']).agg({
            'price': ['sum', 'mean']
        }).reset_index()
        budget_utilization.columns = ['Buyer', 'Round', 'Total Spent', 'Average Price']
        budget_utilization['Budget'] = budget_utilization['Round'].map({1: 100, 2: 150, 3: 150})
        budget_utilization['Utilization Rate'] = (budget_utilization['Total Spent'] / budget_utilization['Budget'] * 100).round(1)
        st.dataframe(budget_utilization)

        # 2. 买家偏好分析
        st.write("### Buyer Preferences")
        
        # 类型偏好
        st.write("#### Type Preferences by Buyer")
        type_pref = pd.crosstab(results_df['buyer'], results_df['type'])
        type_pref_pct = type_pref.div(type_pref.sum(axis=1), axis=0) * 100
        fig_type_pref = px.bar(type_pref_pct, 
                              title='Property Type Selection by Buyer (%)',
                              barmode='group')
        st.plotly_chart(fig_type_pref)

        # 层级偏好
        st.write("#### Tier Preferences by Buyer")
        tier_pref = pd.crosstab(results_df['buyer'], results_df['tier'])
        tier_pref_pct = tier_pref.div(tier_pref.sum(axis=1), axis=0) * 100
        fig_tier_pref = px.bar(tier_pref_pct, 
                              title='Property Tier Selection by Buyer (%)',
                              barmode='group')
        st.plotly_chart(fig_tier_pref)

        # 3. 价格趋势
        st.write("### Price Trends")
        avg_price_trend = results_df.groupby(['buyer', 'round'])['price'].mean().reset_index()
        fig_price_trend = px.line(avg_price_trend, 
                                x='round', 
                                y='price', 
                                color='buyer',
                                title='Average Price Paid by Buyer Over Rounds',
                                labels={'price': 'Average Price', 'round': 'Round'})
        st.plotly_chart(fig_price_trend)

        # 4. 买家行为总结
        st.write("### Buyer Behavior Summary")
        for buyer in results_df['buyer'].unique():
            buyer_data = results_df[results_df['buyer'] == buyer]
            st.write(f"#### Buyer {buyer}")
            
            # 计算统计数据
            total_spent = buyer_data['price'].sum()
            avg_price = buyer_data['price'].mean()
            preferred_type = buyer_data['type'].mode().iloc[0]
            preferred_tier = buyer_data['tier'].mode().iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"- Total spent: ${total_spent}")
                st.write(f"- Average price: ${avg_price:.2f}")
            with col2:
                st.write(f"- Preferred type: {preferred_type}")
                st.write(f"- Preferred tier: {preferred_tier}")

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

if __name__ == "__main__":
    main() 