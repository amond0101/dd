// index.js - 메인 페이지 JavaScript 기능

// 페이지 로드 시 장바구니 카운트 업데이트
document.addEventListener('DOMContentLoaded', function() {
    // 세션 스토리지에서 장바구니 카운트 가져오기
    var cartCount = localStorage.getItem('cartCount') || 0;
    updateCartCount(cartCount);
  });
  
  // 장바구니에 상품 추가
  function addToCart(menuId) {
    // 이벤트 전파 방지 (링크 클릭 방지)
    event.stopPropagation();
    event.preventDefault();
    
    // API 호출
    fetch('/cart/add/' + menuId, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ menu_id: menuId, quantity: 1 })
    })
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      if (data.success) {
        // 장바구니 카운트 업데이트
        updateCartCount(data.cart_count);
        
        // 성공 메시지 표시
        showAddToCartMessage(menuId);
        
        // 로컬 스토리지에 저장
        localStorage.setItem('cartCount', data.cart_count);
      }
    });
  }
  
  // 장바구니 카운트 업데이트
  function updateCartCount(count) {
    document.getElementById('cart-count').textContent = count;
  }
  
  // 장바구니 담기 성공 메시지
  function showAddToCartMessage(menuId) {
    // 메시지 요소 생성
    var messageEl = document.createElement('div');
    messageEl.className = 'cart-message';
    messageEl.innerHTML = 
      '<i class="fa-solid fa-check"></i> 장바구니에 추가되었습니다.' +
      '<a href="/cart" class="view-cart-link">장바구니 보기</a>';
    
    // 메뉴 아이템에 메시지 추가
    var menuItem = document.querySelector('.menu-item-container button[onclick*="' + menuId + '"]').closest('.menu-item-container');
    menuItem.appendChild(messageEl);
    
    // 일정 시간 후 메시지 제거
    setTimeout(function() {
      messageEl.style.opacity = '0';
      setTimeout(function() {
        messageEl.remove();
      }, 300);
    }, 2000);
  }