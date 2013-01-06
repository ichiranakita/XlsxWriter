###############################################################################
#
# Worksheet - A class for writing Excel Worksheets.
#
# Copyright 2013, John McNamara, jmcnamara@cpan.org
#

import xmlwriter


class Worksheet(xmlwriter.XMLwriter):
    """
    A class for writing Excel Worksheets.

    """

    ###########################################################################
    #
    # Public API.
    #
    ###########################################################################

    def __init__(self):
        """
        Constructor.

        """

        super(Worksheet, self).__init__()

        self.name = None
        self.index = None
        self.activesheet = None
        self.firstsheet = None
        self.str_total = None
        self.str_unique = None
        self.str_table = None
        self.table_count = None
        self.date_1904 = None
        self.palette = None
        self.optimization = 0
        self.tempdir = None

        self.ext_sheets = []
        self.fileclosed = 0
        self.excel_version = 2007

        self.xls_rowmax = 1048576
        self.xls_colmax = 16384
        self.xls_strmax = 32767
        self.dim_rowmin = None
        self.dim_rowmax = None
        self.dim_colmin = None
        self.dim_colmax = None

        self.colinfo = []
        self.selections = []
        self.hidden = 0
        self.active = 0
        self.tab_color = 0

        self.panes = []
        self.active_pane = 3
        self.selected = 0

        self.page_setup_changed = 0
        self.paper_size = 0
        self.orientation = 1

        self.print_options_changed = 0
        self.hcenter = 0
        self.vcenter = 0
        self.print_gridlines = 0
        self.screen_gridlines = 1
        self.print_headers = 0

        self.header_footer_changed = 0
        self.header = ''
        self.footer = ''

        self.margin_left = 0.7
        self.margin_right = 0.7
        self.margin_top = 0.75
        self.margin_bottom = 0.75
        self.margin_header = 0.3
        self.margin_footer = 0.3

        self.repeat_rows = ''
        self.repeat_cols = ''
        self.print_area = ''

        self.page_order = 0
        self.black_white = 0
        self.draft_quality = 0
        self.print_comments = 0
        self.page_start = 0

        self.fit_page = 0
        self.fit_width = 0
        self.fit_height = 0

        self.hbreaks = []
        self.vbreaks = []

        self.protect = 0
        self.password = None

        self.set_cols = {}
        self.set_rows = {}

        self.zoom = 100
        self.zoom_scale_normal = 1
        self.print_scale = 100
        self.right_to_left = 0
        self.show_zeros = 1
        self.leading_zeros = 0

        self.outline_row_level = 0
        self.outline_col_level = 0
        self.outline_style = 0
        self.outline_below = 1
        self.outline_right = 1
        self.outline_on = 1
        self.outline_changed = 0

        self.default_row_height = 15
        self.default_row_zeroed = 0

        self.names = {}
        self.write_match = []
        self.table = {}
        self.merge = []

        self.has_vml = 0
        self.has_comments = 0
        self.comments = {}
        self.comments_array = []
        self.comments_author = ''
        self.comments_visible = 0
        self.vml_shape_id = 1024
        self.buttons_array = []

        self.autofilter = ''
        self.filter_on = 0
        self.filter_range = []
        self.filter_cols = {}

        self.col_sizes = {}
        self.row_sizes = {}
        self.col_formats = {}
        self.col_size_changed = 0
        self.row_size_changed = 0

        self.last_shape_id = 1
        self.rel_count = 0
        self.hlink_count = 0
        self.hlink_refs = []
        self.external_hyper_links = []
        self.external_drawing_links = []
        self.external_comment_links = []
        self.external_vml_links = []
        self.external_table_links = []
        self.drawing_links = []
        self.charts = []
        self.images = []
        self.tables = []
        self.sparklines = []
        self.shapes = []
        self.shape_hash = {}
        self.drawing = 0

        self.rstring = ''
        self.previous_row = 0

        self.validations = []
        self.cond_formats = {}
        self.dxf_priority = 1

    # Set this worksheet as a selected worksheet, i.e. the worksheet has
    # its tab highlighted.
    def select(self):
        """
        The ``select()`` method is used to indicate that a worksheet
        is selected in a multi-sheet workbook::

            worksheet1.activate()
            worksheet2.select()
            worksheet3.select()

        A selected worksheet has its tab highlighted. Selecting
        worksheets is a way of grouping them together so that, for
        example, several worksheets could be printed in one go. A
        worksheet that has been activated via the ``activate()``
        method will also appear as selected.

        """
        self.selected = 1

        # A selected worksheet can't be hidden.
        self.hidden = 0

    ###########################################################################
    #
    # Private API.
    #
    ###########################################################################

    def _assemble_xml_file(self):
        # Assemble and write the XML file.

        # Write the XML declaration.
        self._xml_declaration()

        # Write the worksheet element.
        self._write_worksheet()

        # Write the dimension element.
        self._write_dimension()

        # Write the sheetViews element.
        self._write_sheet_views()

        # Write the sheetFormatPr element.
        self._write_sheet_format_pr()

        # Write the sheetData element.
        self._write_sheet_data()

        # Write the pageMargins element.
        self._write_page_margins()

        # Close the worksheet tag.
        self._xml_end_tag('worksheet')

    ###########################################################################
    #
    # XML methods.
    #
    ###########################################################################

    def _write_worksheet(self):
        # Write the <worksheet> element. This is the root element.

        schema = 'http://schemas.openxmlformats.org/'
        xmlns = schema + 'spreadsheetml/2006/main'
        xmlns_r = schema + 'officeDocument/2006/relationships'
        xmlns_mc = schema + 'markup-compatibility/2006'
        ms_schema = 'http://schemas.microsoft.com/'
        xmlns_mv = 'urn:schemas-microsoft-com:mac:vml'
        mc_ignorable = 'mv'
        mc_preserve_attributes = 'mv:*'

        attributes = [
            ('xmlns', xmlns),
            ('xmlns:r', xmlns_r),
        ]

        # TODO Add to constructor
        self.excel_version = 2007

        # Add some extra attributes for Excel 2010. Mainly for sparklines.
        if self.excel_version == 2010:
            attributes.append(('xmlns:mc',
                               schema + 'markup-compatibility/2006'))
            attributes.append(('xmlns:x14ac',
                               ms_schema + 'office/spreadsheetml/2009/9/ac'))
            attributes.append(('mc:Ignorable', 'x14ac'))

        self._xml_start_tag('worksheet', attributes)

    def _write_dimension(self):
        # Write the <dimension> element.
        ref = 'A1'

        attributes = [('ref', ref)]

        self._xml_empty_tag('dimension', attributes)

    def _write_sheet_views(self):
        # Write the <sheetViews> element.
        self._xml_start_tag('sheetViews')

        # Write the sheetView element.
        self._write_sheet_view()

        self._xml_end_tag('sheetViews')

    def _write_sheet_view(self):
        # Write the <sheetView> element.
        tab_selected = '1'
        workbook_view_id = '0'

        attributes = [
            ('tabSelected', tab_selected),
            ('workbookViewId', workbook_view_id),
        ]

        self._xml_empty_tag('sheetView', attributes)

    def _write_sheet_format_pr(self):
        # Write the <sheetFormatPr> element.
        default_row_height = '15'

        attributes = [('defaultRowHeight', default_row_height)]

        self._xml_empty_tag('sheetFormatPr', attributes)

    def _write_sheet_data(self):
        # Write the <sheetData> element.
        self._xml_empty_tag('sheetData')

    def _write_page_margins(self):
        # Write the <pageMargins> element.
        left = '0.7'
        right = '0.7'
        top = '0.75'
        bottom = '0.75'
        header = '0.3'
        footer = '0.3'

        attributes = [
            ('left',   left),
            ('right',  right),
            ('top',    top),
            ('bottom', bottom),
            ('header', header),
            ('footer', footer),
        ]

        self._xml_empty_tag('pageMargins', attributes)
