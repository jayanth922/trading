def test_generate_signals():
    data = pd.DataFrame({'SMA_50': [1, 2, 3], 'SMA_200': [3, 2, 1]})
    data = generate_signals(data)
    assert data['Signal'].iloc[0] == -1
    assert data['Signal'].iloc[2] == 1