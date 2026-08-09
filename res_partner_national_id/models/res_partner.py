# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    national_id = fields.Char(
        string='رقم البطاقة',
        copy=False,
        index='btree',
        tracking=True,
        help='رقم البطاقة الشخصية / رقم الهوية الخاص بالعميل - لازم يكون فريد ومتكررش مع أي عميل تاني.',
    )

    _sql_constraints = [
        (
            'national_id_uniq',
            'unique(national_id)',
            'رقم البطاقة ده مسجل بالفعل مع عميل آخر! برجاء إدخال رقم بطاقة مختلف.',
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._normalize_national_id(vals)
        return super().create(vals_list)

    def write(self, vals):
        self._normalize_national_id(vals)
        return super().write(vals)

    @staticmethod
    def _normalize_national_id(vals):
        """يحول القيمة الفاضية '' لـ False عشان الـ Unique constraint متتأثرش
        بالسجلات اللي معندهاش رقم بطاقة (Postgres بيسمح بأكتر من NULL في unique)."""
        if 'national_id' in vals:
            value = vals.get('national_id')
            if value:
                value = value.strip()
            vals['national_id'] = value or False

    @api.constrains('national_id')
    def _check_national_id_unique(self):
        # حماية إضافية على مستوى الـ Python بجانب الـ SQL Constraint
        # (بتدي رسالة خطأ واضحة بدل رسالة الـ Postgres الافتراضية في بعض الحالات).
        for partner in self:
            if not partner.national_id:
                continue
            duplicate = self.search(
                [
                    ('id', '!=', partner.id),
                    ('national_id', '=', partner.national_id),
                ],
                limit=1,
            )
            if duplicate:
                raise ValidationError(
                    _(
                        'رقم البطاقة "%(national_id)s" مستخدم بالفعل مع العميل "%(partner_name)s". '
                        'برجاء إدخال رقم بطاقة مختلف.',
                        national_id=partner.national_id,
                        partner_name=duplicate.display_name,
                    )
                )

    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', limit=None, order=None):
        """يخلي البحث عن العميل شغال برقم البطاقة في أي حتة بتستخدم name_search
        (زي حقول Many2one لاختيار العميل في الفواتير، أوامر البيع، الدفعات... إلخ)."""
        domain = domain or []
        if name:
            search_domain = ['|', ('name', operator, name), ('national_id', operator, name)]
            return self._search(search_domain + domain, limit=limit, order=order)
        return super()._name_search(name=name, domain=domain, operator=operator, limit=limit, order=order)
