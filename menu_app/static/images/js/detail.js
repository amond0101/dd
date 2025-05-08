// detail.js - 상세 페이지 JavaScript 기능

// 수량 변경 함수
function changeQuantity(change) {
    var quantityInput = document.getElementById('quantity');
    var newQuantity = parseInt(quantityInput.value) + change;
    
    // 최소 1, 최대 10 제한
    if (newQuantity < 1) newQuantity = 1;
    if (newQuantity > 10) newQuantity = 10;
    
    quantityInput.value = newQuantity;
  }
  
  // 수량 유효성 검사
  function validateQuantity() {
    var quantityInput = document.getElementById('quantity');
    var value = parseInt(quantityInput.value);
    
    if (isNaN(value) || value < 1) value = 1;
    if (value > 10) value = 10;
    
    quantityInput.value = value;
  }
  
  // 장바구니에 상품 추가
  function addToCart(menuId) {
    var quantity = parseInt(document.getElementById('quantity').value);
    
    // API 호출
    fetch('/cart/add/' + menuId, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ menu_id: menuId, quantity: quantity })
    })
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      if (data.success) {
        // 장바구니 카운트 업데이트 (헤더에 있을 경우)
        var cartCountEl = document.getElementById('cart-count');
        if (cartCountEl) cartCountEl.textContent = data.cart_count;
        
        // 성공 메시지 표시
        var messageEl = document.createElement('div');
        messageEl.className = 'cart-message';
        messageEl.innerHTML = 
          '<i class="fa-solid fa-check"></i> 상품이 장바구니에 추가되었습니다.' +
          '<a href="/cart" class="view-cart-link">장바구니 보기</a>';
        
        // 기존 메시지 제거 후 새 메시지 추가
        var existingMsg = document.querySelector('.cart-message');
        if (existingMsg) existingMsg.remove();
        
        document.querySelector('.cart-section').appendChild(messageEl);
        
        // 로컬 스토리지에 장바구니 카운트 저장
        localStorage.setItem('cartCount', data.cart_count);
      }
    });
  }