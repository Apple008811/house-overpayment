import streamlit as st
import pandas as pd
import numpy as np

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
if 'current_house_index' not in st.session_state:
    st.session_state.current_house_index = 0
if 'purchased_houses' not in st.session_state:
    st.session_state.purchased_houses = []
if 'available_houses' not in st.session_state:
    st.session_state.available_houses = None
if 'viewed_houses' not in st.session_state:
    st.session_state.viewed_houses = []
if 'viewed_benchmarks' not in st.session_state:
    st.session_state.viewed_benchmarks = []

# 创建示例房产数据
def create_house_data():
    houses = [
        # Value tier
        {"id": 1, "price": 90, "tier": "Value", "type": "Location", "features": "Basic location", "benchmark": 85},
        {"id": 2, "price": 100, "tier": "Value", "type": "Property", "features": "Standard features", "benchmark": None},
        # Median tier
        {"id": 3, "price": 115, "tier": "Median", "type": "Location", "features": "Commercial area", "benchmark": 110},
        {"id": 4, "price": 115, "tier": "Median", "type": "Property", "features": "Larger space", "benchmark": None},
        {"id": 5, "price": 125, "tier": "Median", "type": "Location", "features": "Business zone", "benchmark": 120},
        {"id": 6, "price": 125, "tier": "Median", "type": "Property", "features": "Modern amenities", "benchmark": None},
        # Premium tier
        {"id": 7, "price": 140, "tier": "Premium", "type": "Location", "features": "School district", "benchmark": 135},
        {"id": 8, "price": 140, "tier": "Premium", "type": "Property", "features": "Functional backyard", "benchmark": None}
    ]
    return pd.DataFrame(houses)

# 显示单个房源
def display_house(house, is_current=False):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write(f"### House {house['id']}")
        st.write(f"**Type:** {house['type']}")
        st.write(f"**Tier:** {house['tier']}")
        st.write(f"**Features:** {house['features']}")
        st.write(f"**Price:** ${house['price']}")
        
        # 如果是Location类型且已查看benchmark，显示benchmark
        if house['type'] == 'Location' and house['id'] in st.session_state.viewed_benchmarks:
            st.write(f"**Benchmark:** ${house['benchmark']}")
    
    with col2:
        # 如果是Location类型且未查看benchmark，显示View Benchmark按钮
        if house['type'] == 'Location' and house['id'] not in st.session_state.viewed_benchmarks:
            if st.button(f"View Benchmark (House {house['id']})", 
                        key=f"benchmark_{house['id']}_{is_current}"):
                st.session_state.viewed_benchmarks.append(house['id'])
                st.experimental_rerun()
        
        # 如果房子未被购买，显示Purchase按钮
        if house['id'] not in [h['id'] for h in st.session_state.purchased_houses]:
            if st.button(f"Purchase House {house['id']}", 
                        key=f"purchase_{house['id']}_{is_current}"):
                if house['price'] <= st.session_state.budget:
                    st.session_state.purchased_houses.append({
                        'id': house['id'],
                        'price': house['price'],
                        'tier': house['tier'],
                        'type': house['type'],
                        'round': st.session_state.current_round
                    })
                    st.success(f"Successfully purchased House {house['id']}!")
                    if is_current:
                        st.session_state.current_house_index += 1
                        st.experimental_rerun()
                else:
                    st.error("Insufficient budget!")

# 显示当前房产和历史房源
def display_houses():
    if st.session_state.available_houses is None:
        houses_df = create_house_data()
        # 随机打乱房源顺序
        st.session_state.available_houses = houses_df.sample(frac=1).reset_index(drop=True)
    
    # 显示当前房源
    if st.session_state.current_house_index < len(st.session_state.available_houses):
        st.write("## Current House")
        current_house = st.session_state.available_houses.iloc[st.session_state.current_house_index]
        display_house(current_house, is_current=True)
        
        # 添加Skip按钮
        if st.button("Skip Current House", key=f"skip_{st.session_state.current_house_index}"):
            # 将当前房源添加到已查看列表
            if current_house['id'] not in [h['id'] for h in st.session_state.viewed_houses]:
                st.session_state.viewed_houses.append(current_house.to_dict())
            # 移动到下一个房源
            st.session_state.current_house_index += 1
            st.experimental_rerun()
        
        # 将当前房源添加到已查看列表（如果还没有添加）
        if current_house['id'] not in [h['id'] for h in st.session_state.viewed_houses]:
            st.session_state.viewed_houses.append(current_house.to_dict())
    
    # 如果已经看完所有房源，显示Next Round按钮
    if st.session_state.current_house_index >= len(st.session_state.available_houses):
        st.write("### No more houses available in this round")
        if st.button("Next Round", key=f"next_round_{st.session_state.current_round}"):
            if st.session_state.current_round < 3:
                st.session_state.current_round += 1
                st.session_state.budget = 150
                st.session_state.current_house_index = 0
                st.session_state.available_houses = None
                st.session_state.viewed_houses = []
                st.session_state.viewed_benchmarks = []
                st.experimental_rerun()
            else:
                st.success("Experiment completed! You can now view the simulation results.")
                st.session_state.experiment_completed = True
    
    # 显示历史房源（不包括当前房源）
    if len(st.session_state.viewed_houses) > 1:  # 如果有多于一个已查看的房源
        st.write("## Previously Viewed Houses")
        # 显示除了当前房源之外的所有历史房源
        for house in st.session_state.viewed_houses[:-1]:
            st.write("---")
            display_house(house)

# 主界面
def main():
    st.title("House Buying Experiment")
    
    # 显示当前轮次和预算
    st.sidebar.write(f"### Round: {st.session_state.current_round}/3")
    st.sidebar.write(f"### Budget: ${st.session_state.budget}")
    st.sidebar.write(f"### Houses Purchased: {len(st.session_state.purchased_houses)}")
    
    # 显示实验说明
    with st.expander("Experiment Instructions", expanded=True):
        st.write("""
        ### Instructions
        1. You have 3 rounds to purchase houses
        2. Round 1: Budget = $100
        3. Round 2-3: Budget = $150
        4. Houses will be shown one at a time
        5. Location type houses have benchmarks you can view
        6. Previously viewed houses remain visible
        7. You can purchase any viewed house at any time
        8. Make strategic decisions based on your budget
        """)
    
    # 显示房产
    display_houses()
    
    # 显示每轮的购买记录
    if st.session_state.purchased_houses:
        st.write("### Your Purchase History")
        for round_num in range(1, st.session_state.current_round + 1):
            round_purchases = [p for p in st.session_state.purchased_houses if p['round'] == round_num]
            if round_purchases:
                st.write(f"#### Round {round_num} Purchases")
                df = pd.DataFrame(round_purchases)
                # 重新排列列的顺序
                df = df[['id', 'price', 'tier', 'type', 'round']]
                # 美化列名
                df.columns = ['House ID', 'Price ($)', 'Tier', 'Type', 'Round']
                st.dataframe(df, hide_index=True)
            else:
                st.write(f"#### Round {round_num}: No purchases made")

if __name__ == "__main__":
    main() 