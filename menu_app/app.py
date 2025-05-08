import os
import json
import time
from flask import (
    Flask, render_template, redirect,
    url_for, request, flash, jsonify, session
)
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# .env 파일을 로드해서 환경 변수를 설정
load_dotenv()

app = Flask(__name__)
# FLASK_SECRET 은 .env 에 설정해 두세요
app.secret_key = os.getenv("FLASK_SECRET", "change_me")

# -------------------------------------------------
# 설정
# -------------------------------------------------
ADMIN_FILE      = 'admin.json'
UPLOAD_FOLDER   = 'static/images'
ALLOWED_EXT     = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# -------------------------------------------------
# 초기 메뉴 데이터 (14개)
# -------------------------------------------------
menu_items = [
    { 'id': 1,  'name': '불고기 비빔밥', 'price': 9000,  'description': '신선한 야채와 불고기가 어우러진 비빔밥',   'allergies': ['유제품 알러지','콩 알러지'],                  'image_url': '/static/images/bibimbap.jpg'      },
    { 'id': 2,  'name': '해물파전',     'price': 12000, 'description': '각종 해산물이 들어간 바삭한 파전',          'allergies': ['해산물 알러지','밀 알러지','난류 알러지'],    'image_url': '/static/images/pajeon.jpg'         },
    { 'id': 3,  'name': '김치찌개',     'price': 8000,  'description': '매콤한 김치와 돼지고기가 들어간 찌개',      'allergies': ['해산물 알러지'],                            'image_url': '/static/images/kimchi_jjigae.jpg'  },
    { 'id': 4,  'name': '잡채',         'price': 15000, 'description': '당면과 각종 채소, 고기가 어우러진 잡채',    'allergies': ['밀 알러지','콩 알러지'],                  'image_url': '/static/images/japchae.jpg'         },
    { 'id': 5,  'name': '메밀 국수',    'price': 8500,  'description': '시원한 육수의 메밀 국수',                 'allergies': ['메밀 알러지','난류 알러지'],                'image_url': '/static/images/memil_guksu.jpg'     },
    { 'id': 6,  'name': '견과류 샐러드','price': 7000,  'description': '신선한 채소와 견과류가 들어간 샐러드',      'allergies': ['견과류 알러지'],                           'image_url': '/static/images/salad.jpg'           },
    { 'id': 7,  'name': '두부조림',     'price': 7000,  'description': '부드러운 두부와 매콤한 양념의 조화',      'allergies': ['콩 알러지'],                               'image_url': '/static/images/dubu_jorim.jpg'      },
    { 'id': 8,  'name': '갈비탕',       'price': 11000, 'description': '진하게 우려낸 소갈비 육수',                'allergies': ['유제품 알러지'],                           'image_url': '/static/images/galbitang.jpg'       },
    { 'id': 9,  'name': '계란말이',     'price': 6000,  'description': '부드럽고 촉촉한 계란말이',                'allergies': ['난류 알러지'],                             'image_url': '/static/images/gyeran_mari.jpg'     },
    { 'id': 10, 'name': '오징어볶음',   'price': 9500,  'description': '매콤하게 볶은 오징어와 채소',              'allergies': ['해산물 알러지'],                           'image_url': '/static/images/ojingeo_bokkeum.jpg' },
    { 'id': 11, 'name': '된장찌개',     'price': 8500,  'description': '구수한 된장과 야채가 어우러진 찌개',       'allergies': ['콩 알러지'],                               'image_url': '/static/images/doenjang_jjigae.jpg' },
    { 'id': 12, 'name': '치즈돈까스',   'price': 10000, 'description': '치즈가 듬뿍 들어간 바삭한 돈까스',        'allergies': ['유제품 알러지','밀 알러지','난류 알러지'], 'image_url': '/static/images/cheese_donkatsu.jpg' },
    { 'id': 13, 'name': '쌀국수',       'price': 9000,  'description': '진한 육수와 쌀국수의 조화',              'allergies': [],                                         'image_url': '/static/images/pho.jpg'             },
    { 'id': 14, 'name': '카레라이스',   'price': 8000,  'description': '한국식 매콤한 카레와 밥',                'allergies': ['밀 알러지'],                               'image_url': '/static/images/curry_rice.jpg'      }
]

def get_allergies():
    return sorted({a for item in menu_items for a in item['allergies']})

def allowed_file(fn):
    return '.' in fn and fn.rsplit('.',1)[1].lower() in ALLOWED_EXT

def load_password():
    if not os.path.exists(ADMIN_FILE):
        save_password('12345')
    with open(ADMIN_FILE, 'r', encoding='utf-8') as f:
        return json.load(f).get('password','12345')

def save_password(pw):
    with open(ADMIN_FILE,'w',encoding='utf-8') as f:
        json.dump({'password':pw},f,ensure_ascii=False)

# ── 라우트 ──

@app.route('/')
def index():
    selected = request.args.get('allergy')
    allergies = get_allergies()
    
    # 알레르기 필터링 로직 변경 - 선택한 알레르기가 없는 음식만 필터링
    if selected:
        menu = [m for m in menu_items if selected not in m['allergies']]
    else:
        menu = menu_items
    
    return render_template('index.html',
                           menu_items=menu,
                           allergies=allergies,
                           selected_allergy=selected)

@app.route('/menu/<int:menu_id>')
def menu_detail(menu_id):
    item = next((m for m in menu_items if m['id']==menu_id), None)
    return render_template('detail.html', menu_item=item) if item else redirect(url_for('index'))

@app.route('/add', methods=['GET','POST'])
def add_food():
    if request.method=='POST':
        if request.form.get('admin_password') != load_password():
            flash('관리자 비밀번호가 틀렸습니다.','danger')
            return redirect(url_for('add_food'))
        name        = request.form['name']
        price       = int(request.form['price'])
        desc        = request.form['description']
        allergies   = request.form.getlist('allergies')
        img         = request.files.get('image')
        if img and allowed_file(img.filename):
            fn = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'],fn))
            url = f'/static/images/{fn}'
        else:
            url = '/static/images/default.jpg'
        new_id = max(m['id'] for m in menu_items)+1
        menu_items.append({
            'id':new_id,'name':name,'price':price,
            'description':desc,'allergies':allergies,
            'image_url':url
        })
        flash('음식이 추가되었습니다!','success')
        return redirect(url_for('index'))
    return render_template('add_food.html', allergies=get_allergies())

@app.route('/change-password', methods=['GET','POST'])
def change_password():
    if request.method=='POST':
        cur = request.form['current_password']
        nw  = request.form['new_password']
        cf  = request.form['confirm_password']
        if cur!=load_password():
            flash('현재 비밀번호가 틀렸습니다.','danger')
        elif nw!=cf:
            flash('새 비밀번호가 일치하지 않습니다.','danger')
        else:
            save_password(nw)
            flash('비밀번호가 변경되었습니다!','success')
            return redirect(url_for('index'))
    return render_template('change_password.html')

# ---- 장바구니 관련 라우트 ----

# 장바구니 초기화
@app.route('/cart/init', methods=['POST'])
def init_cart():
    session['cart'] = []
    return jsonify({'success': True})

# 장바구니에 상품 추가
@app.route('/cart/add/<int:menu_id>', methods=['POST'])
def add_to_cart(menu_id):
    quantity = int(request.json.get('quantity', 1))
    
    # 장바구니가 없으면 초기화
    if 'cart' not in session:
        session['cart'] = []
    
    # 메뉴 아이템 찾기
    item = next((m for m in menu_items if m['id'] == menu_id), None)
    if not item:
        return jsonify({'success': False, 'message': '메뉴를 찾을 수 없습니다.'})
    
    # 장바구니에 이미 있는지 확인
    cart_item = next((c for c in session['cart'] if c['id'] == menu_id), None)
    if cart_item:
        cart_item['quantity'] += quantity
    else:
        # 장바구니에 추가
        cart_item = {
            'id': item['id'],
            'name': item['name'],
            'price': item['price'],
            'quantity': quantity,
            'allergies': item['allergies'],
            'image_url': item['image_url']
        }
        session['cart'].append(cart_item)
    
    # 세션 변경 표시
    session.modified = True
    
    return jsonify({
        'success': True, 
        'item': cart_item,
        'cart_count': sum(c['quantity'] for c in session['cart'])
    })

# 장바구니 조회
@app.route('/cart', methods=['GET'])
def view_cart():
    cart = session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)

# 장바구니 항목 수량 변경
@app.route('/cart/update/<int:menu_id>', methods=['POST'])
def update_cart(menu_id):
    quantity = int(request.json.get('quantity'))
    
    if 'cart' not in session:
        return jsonify({'success': False, 'message': '장바구니가 비어있습니다.'})
    
    # 장바구니 항목 찾기
    cart_item = next((c for c in session['cart'] if c['id'] == menu_id), None)
    if not cart_item:
        return jsonify({'success': False, 'message': '장바구니에 해당 항목이 없습니다.'})
    
    if quantity <= 0:
        # 항목 삭제
        session['cart'] = [c for c in session['cart'] if c['id'] != menu_id]
    else:
        # 수량 업데이트
        cart_item['quantity'] = quantity
    
    # 세션 변경 표시
    session.modified = True
    
    # 새로운 합계 계산
    total_price = sum(item['price'] * item['quantity'] for item in session['cart'])
    
    return jsonify({
        'success': True,
        'cart_count': sum(c['quantity'] for c in session['cart']),
        'total_price': total_price
    })

# 장바구니 비우기
@app.route('/cart/clear', methods=['POST'])
def clear_cart():
    session['cart'] = []
    session.modified = True
    return jsonify({'success': True})

# 알러지 필터링 처리 (장바구니 결제 페이지용)
@app.route('/cart/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        allergies = request.form.getlist('allergies')
        cart = session.get('cart', [])
        
        # 알러지 있는 제품 제외
        if allergies:
            filtered_cart = []
            for item in cart:
                if not any(allergy in item['allergies'] for allergy in allergies):
                    filtered_cart.append(item)
            
            # 필터링된 장바구니 저장
            session['cart'] = filtered_cart
            session.modified = True
            
            # 결제 페이지로 리다이렉트
            return redirect(url_for('payment'))
        
        # 알러지 선택 안 한 경우 그대로 결제 페이지로
        return redirect(url_for('payment'))
        
    # GET 요청 - 체크아웃 페이지 표시
    cart = session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    allergies = get_allergies()
    
    return render_template('checkout.html', 
                          cart=cart, 
                          total_price=total_price, 
                          allergies=allergies)

# 결제 페이지 (예시)
@app.route('/payment')
def payment():
    cart = session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('payment.html', cart=cart, total_price=total_price)

if __name__=='__main__':
    if not os.path.exists(ADMIN_FILE):
        save_password('12345')
    app.run(debug=True, host='0.0.0.0', port=5000)