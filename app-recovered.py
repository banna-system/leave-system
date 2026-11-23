from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leave.db'
app.config['SECRET_KEY'] = 'surat3_leave_system'
db = SQLAlchemy(app)

class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=False)
    total_days = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>ระบบลา โรงเรียนองค์การบริการส่วนจังหวัดสุราษฎร์ธานี ๓ (บ้านนา)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600&display=swap');
        body { font-family: 'Sarabun', sans-serif; background-color: #f4f6f9; color: #000; }
        
        /* จัดขนาดหน้า A4 พอดี 1 หน้ากระดาษสำหรับการพิมพ์ */
        .official-form { 
            background: white; 
            padding: 25px 40px; 
            border-radius: 6px; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.08); 
            max-width: 800px; 
            margin: 20px auto; 
            font-size: 14px; 
            line-height: 1.5; 
        }
        .table-official th, .table-official td { 
            border: 1px solid #333 !important; 
            padding: 3px 6px; 
            text-align: center; 
            font-size: 12px; 
            vertical-align: middle; 
        }
        .comment-box { 
            border: 1px solid #444; 
            border-radius: 3px; 
            padding: 5px 8px; 
            font-size: 11px; 
            min-height: 45px; 
            margin-bottom: 3px; 
            background-color: #fff; 
        }
        @media print {
            @page { size: A4; margin: 10mm; }
            body { background: white; }
            body * { visibility: hidden; }
            .printable, .printable * { visibility: visible; }
            .printable { 
                position: absolute; 
                left: 0; 
                top: 0; 
                width: 100%; 
                padding: 0; 
                background: white; 
                box-shadow: none; 
                margin: 0; 
                font-size: 13px;
            }
            .no-print { display: none !important; }
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark navbar-expand-lg mb-3 no-print" style="background-color: #0b2f64;">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/" style="font-size: 16px;">🏫 ระบบสารสนเทศงานบุคลากร โรงเรียนอบจ.สฎ. ๓ (บ้านนา)</a>
        </div>
    </nav>

    <div class="container mb-5">
        {% if print_mode %}
        <!-- หน้าฟอร์มใบลาทางการแบบพอดี 1 หน้า A4 -->
        <div class="official-form printable">
            <div class="row align-items-center mb-2">
                <div class="col-2 text-center">
                    <div style="width: 45px; height: 45px; background: #0b2f64; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 12px; margin: auto;">อบจ.</div>
                </div>
                <div class="col-6">
                    <h6 class="mb-0 fw-bold" style="font-size: 15px;">โรงเรียนองค์การบริการส่วนจังหวัดสุราษฎร์ธานี ๓ (บ้านนา)</h6>
                    <span class="text-muted" style="font-size: 12px;">อำเภอบ้านนาเดิม จังหวัดสุราษฎร์ธานี</span>
                </div>
                <div class="col-4 text-end" style="font-size: 12px;">
                    เขียนที่ โรงเรียนอบจ.สฎ.๓ (บ้านนา)<br>
                    วันที่ {{ leave.created_at.strftime('%d') }} เดือน {{ leave.created_at.strftime('%m') }} พ.ศ. {{ leave.created_at.year + 543 }}
                </div>
            </div>

            <hr style="border-top: 1.5px solid #333; opacity: 1; margin: 8px 0;">

            <div class="text-center fw-bold" style="font-size: 18px; margin-bottom: 10px;">
                แบบ{{ leave.leave_type }}
            </div>

            <div class="mb-2" style="font-size: 13px;">
                <p class="mb-1"><strong>เรื่อง:</strong> ขอ{{ leave.leave_type }}</p>
                <p class="mb-2"><strong>เรียน:</strong> ผู้อำนวยการโรงเรียนองค์การบริการส่วนจังหวัดสุราษฎร์ธานี ๓ (บ้านนา)</p>
            </div>

            <p style="text-indent: 30px; text-align: justify; margin-bottom: 10px;">
                ข้าพเจ้า <strong>{{ leave.teacher_name }}</strong> ตำแหน่ง <strong>{{ leave.position }}</strong> สังกัดกลุ่มสาระฯ ฝ่ายบริหารงานบุคคล โรงเรียนอบจ.สฎ.๓ (บ้านนา) 
                มีความประสงค์ขอลา <strong>{{ leave.leave_type }}</strong> เนื่องมาจาก <strong>{{ leave.reason }}</strong> 
                ตั้งแต่วันที่ <strong>{{ leave.start_date }}</strong> ถึงวันที่ <strong>{{ leave.end_date }}</strong> (รวมเป็นเวลา <strong>{{ leave.total_days }}</strong>)
            </p>

            <p style="text-indent: 30px; margin-bottom: 15px;">
                ในระหว่างการลาครั้งนี้ สามารถติดต่อข้าพเจ้าได้ที่ บ้านเลขที่ - ต.บ้านนา อ.บ้านนาเดิม จ.สุราษฎร์ธานี เบอร์โทรศัพท์ <strong>{{ leave.phone }}</strong>
            </p>

            <div class="row mb-2">
                <div class="col-6"></div>
                <div class="col-6 text-center" style="font-size: 13px;">
                    <p style="line-height: 1.4;">
                        ขอแสดงความนับถือ<br><br>
                        ลงชื่อ..........................................................ผู้ขอลา<br>
                        ({{ leave.teacher_name }})<br>
                        ตำแหน่ง {{ leave.position }}
                    </p>
                </div>
            </div>

            <!-- ตารางสถิติและความเห็น (จัดให้กระชับในหน้าเดียว) -->
            <div class="row pt-1 border-top" style="font-size: 11px;">
                <div class="col-md-6">
                    <table class="table table-bordered table-official mb-1">
                        <tr class="table-light"><th colspan="4">สถิติการลาในศกนี้ (ปีงบประมาณ / ปีการศึกษา)</th></tr>
                        <tr><th>ประเภทการลา</th><th>ลามาแล้ว</th><th>ลาครั้งนี้</th><th>รวมเป็น</th></tr>
                        <tr><td>ลาป่วย</td><td>0 วัน</td><td>-</td><td>0 วัน</td></tr>
                        <tr><td>ลากิจส่วนตัว</td><td>0 วัน</td><td>{{ leave.total_days }}</td><td>{{ leave.total_days }}</td></tr>
                        <tr><td>ลาพักผ่อน</td><td>0 วัน</td><td>-</td><td>0 วัน</td></tr>
                    </table>
                    <div class="text-center" style="font-size: 11px;">
                        <p class="mb-1">ลงชื่อ..................................................ผู้ตรวจสอบ<br>(..................................................)<br>เจ้าหน้าที่งานบุคลากรและทะเบียนสถิติ</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="comment-box">
                        <strong>ความเห็นของหัวหน้างานบุคคล:</strong><br>
                        <span class="text-muted">ตรวจสอบภาระงานแล้ว เห็นควรเสนออนุมัติ</span>
                    </div>
                    <div class="text-center" style="font-size: 11px;">
                        <p class="mb-0">ลงชื่อ..................................................หัวหน้างานบุคคล<br>(นางกนกวรรณ ศรีสว่าง)<br>วันที่ ...../...../.....</p>
                    </div>
                </div>
            </div>

            <div class="row mt-1" style="font-size: 11px;">
                <div class="col-md-6">
                    <div class="comment-box">
                        <strong>ความเห็นของรองผู้อำนวยการฝ่ายบริหารงานบุคคล:</strong><br>
                        <span class="text-muted">เห็นควรเสนอผู้อำนวยการสถานศึกษาเพื่อโปรดพิจารณาอนุมัติ</span>
                    </div>
                    <div class="text-center" style="font-size: 11px;">
                        <p class="mb-0">ลงชื่อ..................................................ผู้พิจารณา<br>(นางสาวศิริกาญจน์ บุญมาก)<br>รองผู้อำนวยการสถานศึกษา<br>วันที่ ...../...../.....</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="comment-box" style="min-height: 40px;">
                        <strong style="display: block; margin-bottom: 2px;">คำสั่ง / การพิจารณาอนุมัติ:</strong>
                        [ &nbsp; ] อนุมัติ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ &nbsp; ] ไม่อนุมัติ
                    </div>
                    <div class="text-center" style="font-size: 11px;">
                        <p class="mb-0">ลงชื่อ..................................................ผู้อนุมัติ<br>(นางสาวลักขณาวรรณ เพชรรัตน์)<br>ผอ.โรงเรียนอบจ.สฎ. ๓ (บ้านนา)<br>วันที่ ...../...../.....</p>
                    </div>
                </div>
            </div>

            <div class="text-center mt-3 no-print">
                <button onclick="window.print()" class="btn btn-success px-5 py-2 fw-bold">🖨️ สั่งพิมพ์ใบลาทางการ (พอดี 1 หน้า)</button>
                <a href="/" class="btn btn-secondary px-4 py-2 ms-2">กลับหน้าหลัก</a>
            </div>
        </div>
        {% else %}
        <!-- หน้ากรอกข้อมูล -->
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card shadow border-0">
                    <div class="card-header text-white text-center py-3" style="background-color: #0b2f64;">
                        <h5 class="mb-0 fw-bold">📝 ระบบยื่นใบลา โรงเรียนอบจ.สฎ.๓ (บ้านนา)</h5>
                    </div>
                    <div class="card-body p-4">
                        <form method="POST">
                            <div class="mb-3">
                                <label class="form-label fw-bold">ชื่อ-นามสกุล (ผู้ขอลา)</label>
                                <input type="text" class="form-control" name="teacher_name" required placeholder="เช่น นายสมชาย ใจดี">
                            </div>
                            <div class="mb-3">
                                <label class="form-label fw-bold">ตำแหน่ง</label>
                                <input type="text" class="form-control" name="position" required placeholder="เช่น ครู คศ. 1">
                            </div>
                            <div class="mb-3">
                                <label class="form-label fw-bold">ประเภทการลา</label>
                                <select class="form-select" name="leave_type">
                                    <option value="ลากิจส่วนตัว">ลากิจส่วนตัว</option>
                                    <option value="ลาป่วย">ลาป่วย</option>
                                    <option value="ลาพักผ่อน">ลาพักผ่อน</option>
                                </select>
                            </div>
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label fw-bold">ตั้งแต่วันที่</label>
                                    <input type="date" class="form-control" name="start_date" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label fw-bold">ถึงวันที่</label>
                                    <input type="date" class="form-control" name="end_date" required>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label class="form-label fw-bold">จำนวนวันลา (เช่น 0.5 วัน, 1 วัน)</label>
                                <input type="text" class="form-control" name="total_days" required placeholder="1 วัน">
                            </div>
                            <div class="mb-3">
                                <label class="form-label fw-bold">เหตุผลการลา</label>
                                <textarea class="form-control" name="reason" rows="2" required placeholder="ระบุเหตุผลความจำเป็น..."></textarea>
                            </div>
                            <div class="mb-3">
                                <label class="form-label fw-bold">เบอร์โทรศัพท์ที่ติดต่อได้</label>
                                <input type="text" class="form-control" name="phone" required placeholder="08XXXXXXXX">
                            </div>
                            <button type="submit" class="btn btn-primary w-100 py-2 fw-bold" style="background-color: #0b2f64;">บันทึกข้อมูลและสร้างใบลา</button>
                        </form>
                    </div>
                </div>
            </div>

            <div class="col-md-10 mt-5">
                <div class="card shadow border-0">
                    <div class="card-header bg-dark text-white py-3">
                        <h5 class="mb-0 fw-bold">📊 ประวัติและรายการใบลาทั้งหมดในระบบ</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped align-middle">
                                <thead class="table-secondary">
                                    <tr>
                                        <th>ชื่อ-นามสกุล</th>
                                        <th>ตำแหน่ง</th>
                                        <th>ประเภทการลา</th>
                                        <th>ช่วงเวลา</th>
                                        <th>รวม</th>
                                        <th class="text-center">จัดการ</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for leave in leaves %}
                                    <tr>
                                        <td>{{ leave.teacher_name }}</td>
                                        <td>{{ leave.position }}</td>
                                        <td>{{ leave.leave_type }}</td>
                                        <td>{{ leave.start_date }} ถึง {{ leave.end_date }}</td>
                                        <td><span class="badge bg-success">{{ leave.total_days }}</span></td>
                                        <td class="text-center">
                                            <a href="/print/{{ leave.id }}" class="btn btn-sm btn-outline-primary fw-bold">📄 พิมพ์ใบลา</a>
                                        </td>
                                    </tr>
                                    {% else %}
                                    <tr>
                                        <td colspan="6" class="text-center text-muted py-4">ยังไม่มีรายการลาในระบบ กรุณากรอกข้อมูลด้านบนเพื่อเริ่มใช้งาน</td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_leave = LeaveRequest(
            teacher_name=request.form['teacher_name'],
            position=request.form['position'],
            leave_type=request.form['leave_type'],
            start_date=request.form['start_date'],
            end_date=request.form['end_date'],
            total_days=request.form['total_days'],
            reason=request.form['reason'],
            phone=request.form['phone']
        )
        db.session.add(new_leave)
        db.session.commit()
        return redirect(url_for('index'))
    
    leaves = LeaveRequest.query.order_by(LeaveRequest.id.desc()).all()
    return render_template_string(HTML_TEMPLATE, leaves=leaves, print_mode=False)

@app.route('/print/<int:id>')
def print_leave(id):
    leave = LeaveRequest.query.get_or_404(id)
    return render_template_string(HTML_TEMPLATE, leave=leave, print_mode=True)

if __name__ == '__main__':
    app.run(debug=True)