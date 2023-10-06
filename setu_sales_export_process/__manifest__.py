{'name': "Setu Sales Export Process",
 'version': '16.0',
 'author': "Author Name",
 'category': 'Category',
 'description': "Setu Sales Export Process",
 'depends':['base','sale','uom'],
 'data': ['security/ir.model.access.csv',
          'wizard/setu_new_quotation_creation_view.xml',
          'views/setu_sale_contract_view.xml',
          'views/setu_sale_contract_sequence.xml',
          # 'wizard/setu_new_quotation_creation_view.xml'
          ]
 }