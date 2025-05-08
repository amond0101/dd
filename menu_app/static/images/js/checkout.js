// checkout.js - 체크아웃 페이지 JavaScript 기능

// 알러지 선택에 따른 필터링
function filterItems() {
    // 선택된 알러지 목록 가져오기
    var selectedAllergies = Array.from(document.querySelectorAll('input[name="allergies"]:checked'))
      .map(function(checkbox) { return checkbox.value; });
    
    // 장바구니 항목 필터링
    var cartItems = document.querySelectorAll('.cart-item');
    var totalPrice = 0;
    
    cartItems.forEach(function(item) {
      var itemAllergies = item.dataset.allergies.split(',').filter(function(a) { return a; });
      var itemPrice = parseInt(item.querySelector('.item-total').dataset.price);
      
      // 선택된 알러지가 있는지 확인
      var hasAllergy = selectedAllergies.some(function(allergy) {
        return itemAllergies.includes(allergy);
      });
      
      if (hasAllergy) {
        // 알러지가 있는 항목 페이드 아웃
        item.classList.add('fade-out');
      } else {
        // 알러지가 없는 항목 표시 및 가격 계산
        item.classList.remove('fade-out');
        totalPrice += itemPrice;
      }
    });
    
    // 총 가격 업데이트
    document.getElementById('total-price').textContent = totalPrice;
  }