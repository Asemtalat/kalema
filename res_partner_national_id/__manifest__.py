# -*- coding: utf-8 -*-
{
    'name': 'رقم البطاقة الفريد للعملاء - National ID Unique',
    'version': '19.0.1.0.0',
    'category': 'Contacts',
    'summary': 'إضافة حقل رقم البطاقة (Unique) على العميل مع البحث والفلترة به في كل الشاشات',
    'description': """
رقم البطاقة الفريد للعملاء
===========================
- إضافة حقل جديد "رقم البطاقة" (national_id) على جهة الاتصال (res.partner).
- الحقل فريد (Unique) على مستوى قاعدة البيانات (SQL Constraint) - لا يمكن تكراره إطلاقًا.
- الحقل يظهر في:
    * شاشة فورم العميل (Form).
    * شاشة الليست (List/Tree).
    * شاشة البحث (Search View) وكل الفلاتر.
- إمكانية البحث عن العميل برقم البطاقة من أي مكان في النظام (بما في ذلك حقول Many2one
  زي اختيار العميل في الفواتير / أوامر البيع... إلخ) عن طريق تعديل name_search.
    """,
    'author': 'Octa-Tech',
    'website': 'https://octa-tech.net',
    'license': 'LGPL-3',
    'depends': ['base', 'contacts'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
