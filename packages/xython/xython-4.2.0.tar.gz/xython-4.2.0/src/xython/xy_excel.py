# noinspection PyUnresolvedReferences
import re, math, string, random, os, itertools, copy, chardet
import pywintypes, webbrowser, psutil
import win32gui, win32com.client
import xy_re, xy_color, xy_util, xy_time, xy_common
import ctypes
from ctypes import wintypes
import datetime
from itertools import product

# RECT 구조체 정의
class RECT(ctypes.Structure):
	_fields_ = [
		("left", wintypes.LONG),
		("top", wintypes.LONG),
		("right", wintypes.LONG),
		("right", wintypes.LONG),
		("bottom", wintypes.LONG)
	]

class xy_excel:

	def __getattr__(self, name: str) -> int:
		"""
		동적 속성 접근을 처리하여 메서드를 속성처럼 사용할 수 있게 합니다.

		:param name: 접근하려는 속성 이름 ('activesheet' 또는 'activecell')
		:return: activesheet의 경우 시트 이름, activecell의 경우 셀 값

		Examples
		--------
		.. code-block:: python
        # 메서드 호출 대신 속성처럼 접근
        sheet_name = excel.activesheet
        cell_value = excel.activecell
		"""
		result = ""
		if name == "activesheet":
			result = self.get_activesheet_name()
		if name == "activecell":
			result = self.read_activecell()
		return result

	def __init__(self, filename="", cache_tf=""):
		"""
		__init__는 이 모듈이 실행이 될때 제일 먼저 자동으로 실행이 되는 함수이다

		공통으로 사용할 변수들을 설정
		모든 변수들중에서 공통으로 사용되는것은 self.varx를 이용

		:param filename: (str) 화일의 이름을 나타내는 문자열
		:param cache_tf: (bool) 캐시를 사용할것인지 아닌지를 나타내는 bool
		:return: None
		"""
		self.color = xy_color.xy_color()
		self.util = xy_util.xy_util()
		self.rex = xy_re.xy_re()
		self.timex = xy_time.xy_time()

		self.multi_range = None

		self.value = None
		self.sheet_obj = None
		self.sheet_obj2 = None

		self.range_obj = None
		self.range_obj2 = None

		self.x = None
		self.y = None
		self.x0 = None
		self.y0 = None

		self.x1 = None
		self.y1 = None
		self.x2 = None
		self.y2 = None

		self.x3 = None
		self.y3 = None
		self.x4 = None
		self.y4 = None

		self.xyxy = [self.x1, self.y1, self.y1, self.y2]
		self.xyxy2 = [self.x3, self.y3, self.y4, self.y4]
		self.xy = [self.x, self.y]
		self.xy2 = [self.x0, self.y0]

		self.varx = xy_common.xy_common().varx  # package안에서 공통적으로 사용되는 변수들
		self.varx["setup"] = {}  # setup용 전용 입니다
		self.varx["default"] = {}
		self.varx["pen_color"] = ""
		self.varx["font"] = {}
		self.varx["pen_style"] = 4
		self.varx["pen_thickness"] = 5
		self.varx["start_point_width"] = 2
		self.varx["start_point_length"] = 2
		self.varx["start_point_style"] = 1
		self.varx["end_point_width"] = 2
		self.varx["end_point_length"] = 2
		self.varx["end_point_style"] = 1

		self.border_line = {}

		self.v_line_position = self.varx["check_line_position"]
		self.v_line_style_dic = self.varx["line_style_vs_enum"]
		self.v_line_thickness_dic = self.varx["check_line_thickness"]

		if filename == "no" or filename == "not":  # 화일을 열지 않고 실행시키기위한 부분
			pass
		else:
			self.__start_pcell(filename, cache_tf)

	def __start_pcell(self, filename="", cache_tf=""):
		"""
		엑셀 객체를 초기화하고 워크북을 열거나 생성합니다.

		__init__에서 분리된 내부 메서드로, 실제 엑셀 애플리케이션 연결 및
		워크북 처리를 담당합니다.

		:param filename: 열거나 생성할 파일명 또는 옵션
						- None/""/active: 현재 활성 워크북
						- "new": 새 워크북 생성
						- int: 열린 워크북 중 n번째
						- str: 파일 경로 또는 이름
		:param cache_tf: 캐시 사용 여부 (현재 미사용)
		:return: 워크북 객체
		"""
		try:
			self.xlapp = win32com.client.GetActiveObject("Excel.Application")
		except:
			self.xlapp = win32com.client.dynamic.Dispatch("Excel.Application")

		if isinstance(filename, str): filename = str(filename).lower()

		if filename in [None, "", "activeworkbook", "active_workbook", "active"]:
			if self.xlapp.ActiveWorkbook:
				self.xlbook = self.xlapp.ActiveWorkbook
			else:
				self.xlapp.WindowState = -4137
				self.xlapp.Visible = 1
				self.xlbook = self.xlapp.Workbooks.Add()

		elif filename == "new":
			self.xlapp.WindowState = -4137
			self.xlapp.Visible = 1
			self.xlbook = self.xlapp.Workbooks.Add()

		elif isinstance(filename, int):
			# 이미 열려화일에 같은 화일이름이 있는지 확인
			if filename <= self.xlapp.WorkBooks.Count:
				self.xlbook = self.xlapp.Workbooks[filename - 1]

		elif filename:
			# 이미 열린화일에 같은 화일 이름이 있는지 확인
			file_found = False
			for index in range(self.xlapp.Workbooks.Count):
				short_name = self.xlapp.Workbooks[index].Name
				one_file = self.util.check_file_path(self.xlapp.Workbooks[index].FullName)
				if str(one_file).lower() == str(filename).lower() or str(short_name).lower() == str(filename).lower():
					self.xlbook = self.xlapp.Workbooks[index]
					file_found = True
					break

			# 열려진 화일중에 같은 것이 없으면, 화일을 연다
			if not file_found:
				path = ""
				self.xlapp.WindowState = -4137
				self.xlapp.Visible = 1
				if not "\\" in filename:
					path = os.getcwd().replace('\'', '\\') + '\\'

				if path.endswith('\\'):
					self.xlbook = self.xlapp.Workbooks.Open(path + filename + ".xlsx")
				else:
					self.xlbook = self.xlapp.Workbooks.Open(path + '\\' + filename + ".xlsx")

		# 현재 시트의 제일 큰 가로와 세로열을 설정한다
		self.get_max_x_n_y_for_sheet()
		return self.xlbook

	def activesheet(self):
		"""
		활성화된 시트의 이름을 돌려주는 것

		:return: (str) 활성화된 시트의 이름
		Examples
		--------
		.. code-block:: python
			<object_name>.activesheet()
		"""
		return self.get_activesheet_name()

	def add_num_for_range(self, sheet_name, xyxy, input_value, is_text_tf=True):
		"""
		입력영역의 안의 모든 값에 입력으로 들어온 숫자나 문자를 더하는 것
		에러가 발생을 하면, 그냥 무시하고 다음것을 실행
		add는 현재있는 자료를 변경하거나 추가 삭제할때 사용하는 접두사이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (any) 입력값
		:param is_text_tf: (bool) 문자만 할것인지, 숫자도 문자로 변경해서 할것인지
		:return: None,
		Examples
		--------
		.. code-block:: python
			<object_name>.add_num_for_range(sheet_name="", xyxy="", input_value=2, is_text_tf=True)
			<object_name>.add_num_for_range(sheet_name="", xyxy="", input_value=2)
			<object_name>.add_num_for_range("", "", 2)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		try:
			for x in range(x1, x2 + 1):
				for y in range(y1, y2 + 1):
					one_value = sheet_obj.Cells(x, y).Value
					if not is_text_tf :
						sheet_obj.Cells(x, y).Value = str(one_value) + input_value
					else:
						if isinstance(one_value, str):
							sheet_obj.Cells(x, y).Value = str(one_value) + input_value
		except:
			pass

	def add_text_at_left(self, input_value):
		"""
		선택 영역의 각 셀 값 왼쪽에 텍스트를 추가합니다.

		:param input_value: 추가할 텍스트
		:return: None

		Examples
		--------
		.. code-block:: python
		    excel.select_range("", "A1:A10")
		    excel.add_text_at_left("접두어_")
		"""
		self.add_text(self, input_value, "left")

	def add_text_at_right(self, input_value):
		"""
		선택 영역의 각 셀 값 오른쪽에 텍스트를 추가합니다.

		:param input_value: 추가할 텍스트
		:return: None

		Examples
		--------
		.. code-block:: python
		    excel.select_range("", "A1:A10")
		    excel.add_text_at_right("_접미어")
		"""
		self.add_text(self, input_value, "right")

	def alert_off(self):
		"""
		엑셀 경고 메시지를 비활성화합니다.
		시트 삭제 등의 작업 시 확인 대화상자가 표시되지 않도록 합니다.
		:return: None

		Examples
		--------
		.. code-block:: python
		    excel.alert_off()
		    excel.delete_sheet_by_name("Sheet1")  # 확인 없이 삭제
		    excel.alert_on()  # 작업 후 다시 활성화
		"""
		self.xlapp.DisplayAlerts = False

	def alert_on(self):
		"""
		엑셀 경고 메시지를 활성화합니다.
		:return: None

		Examples
		--------
		.. code-block:: python
		    excel.alert_on()
		"""
		self.xlapp.DisplayAlerts = True

	def align_for_range(self, sheet_name, xyxy, x_align, y_align):
		"""
		선택영역의 값들의 표시되는 형태를 나타내는 것으로, 가로형과 세로형의 형태를 지정하는 것이다
		가로와 세로 방향으로 모두 설정하는 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param x_align: (str) 가로줄의 얼라인먼트를 나타내는 문자열
		:param y_align: (str) 세로줄의 얼라인먼트를 나타내는 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.align_for_range(sheet_name="", xyxy="", x_align="center", y_align="top")
			<object_name>.align_for_range("", [1,1,5,7], "center", "top")
			<object_name>.align_for_range(sheet_name="sht1", xyxy="", x_align="center", y_align="top")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		dic_x = {"right": -4152, "middle": -4108, "center": -4108, "left": -4131, "오른쪽": -4152, "중간": 2, "왼쪽": -4131}
		dic_y = {"middle": -4108, "center": -4108, "top": -4160, "bottom": -4107, "low": -4107, "중간": -4108, "위": -4160,
				 "아래": - 4107}
		if x_align: range_obj.HorizontalAlignment = dic_x[x_align]
		if y_align: range_obj.VerticalAlignment = dic_y[y_align]

	def arrange_columns_by_base_title(self, sheet1, xyxy1, sheet2, xyxy2):
		"""
		sheet1의 제목 순서를 기준으로 sheet2의 열을 재정렬

		:param sheet1:
		:param xyxy1:
		:param sheet2:
		:param xyxy2:
		:return:
		"""
		sheet1_obj = self.check_sheet_name(sheet1)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy1)

		sheet2_obj = self.check_sheet_name(sheet2)
		[x3, y3, x4, y4] = self.change_any_address_to_xyxy(xyxy2)

		# 기준 시트의 제목들을 먼저 모두 읽기
		base_headers = []
		for base_y in range(y1, y2 + 1):
			base_value = sheet1_obj.Cells(x1, base_y).Value
			base_headers.append(base_value)

		# 변경 시트의 제목들을 먼저 모두 읽기
		change_headers = []
		for change_y in range(y3, y4 + 1):
			change_value = sheet2_obj.Cells(x3, change_y).Value
			change_headers.append(change_value)

		# base_headers 순서대로 처리
		for index, base_value in enumerate(base_headers):
			target_pos = y3 + index  # 이동해야 할 목표 위치
			found = False

			# sheet2에서 해당 제목 찾기 (현재 위치부터 끝까지)
			for search_y in range(target_pos, y4 + 1):
				search_value = sheet2_obj.Cells(x3, search_y).Value

				if search_value == base_value:
					found = True
					print(f"  → 발견 위치: {search_y}, 값: {search_value}")

					# 이미 올바른 위치에 있으면 패스
					if search_y == target_pos:
						print(f"  → 이미 올바른 위치")
					else:
						# 열 이동
						print(f"  → 열 이동: {search_y} -> {target_pos}")
						self.move_yline([sheet2, sheet2], [search_y, target_pos])
					break

			# base에는 있지만 change에 없으면 빈 열 삽입
			if not found:
				print(f"  → 없음. 빈 열 삽입: {target_pos}")
				self.insert_yline(sheet2, target_pos)
				y4 += 1  # 전체 범위 확장

	def autofit(self):
		"""
		현재 선택된 영역의 열 너비를 내용에 맞게 자동 조정합니다.

		:return: None

		Examples
		--------
		.. code-block:: python
        excel.select_range("", "A1:C10")
        excel.autofit()
		"""
		new_y1 = self.change_num_to_char(self.y1)
		new_y2 = self.change_num_to_char(self.y2)
		self.sheet_obj.Columns(new_y1 + ':' + new_y2).AutoFit()

	def arrange_sheet_same_with_another_sheet_condition(self, sheet1, xyxy1, sheet2, xyxy2):
		"""
		두개의 시트에서 하나를 기준으로 다른 하나의 시트 내용을 정렬하는것
		첫번째 시트의 제일 윗줄을 기준으로 두번째 시트를 정렬 하는것

		:param sheet1:
		:param xyxy1:
		:param sheet2:
		:param xyxy2:
		:return:
		Examples
		--------
		.. code-block:: python
			<object_name>.arrange_sheet_same_with_another_sheet_condition()
		"""
		self.arrange_columns_by_base_title(sheet1, xyxy1, sheet2, xyxy2)

	def arrange_sheets_by_name(self):
		"""
		현재 워크북의 모든 시트를 이름순으로 정렬하는것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.arrange_sheets_by_name()
		"""
		sheets_name = self.get_sheet_names()
		sheets_name.sort()
		for index, one_value in enumerate(sheets_name):
			self.move_sheet_position_by_no(one_value, index + 1)

	def autofill(self):
		"""
		선택 영역 내에서 빈 셀을 위쪽 셀의 값으로 자동 채웁니다.

		:return: None

		Examples
		--------
		.. code-block:: python
        excel.select_range("", "A1:A10")
        excel.autofill()
		"""
		l2d = self.read()
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			if not l2d[x - self.x1][y - self.y1]:
				if x != self.x1:
					self.sheet_obj.Cells(x, y).Value = l2d[x - self.x1 - 1][y - self.y1]

	def autofill_for_range(self, sheet_name, xyxy):
		"""
		자동채우기 기능이며
		선택된 영역안의 빈곳을 위의 값으로 채우는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.autofill(sheet_name="", xyxy="")
			<object_name>.autofill("sht1", [1,1,3,20])
			<object_name>.autofill("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		l2d = self.read_value_for_range(sheet_name, xyxy)
		for ix, l1d in enumerate(l2d):
			for iy, one_value in enumerate(l1d):
				if not one_value and ix != 0:
					self.sheet_obj.Cells(x1+ix, y1+iy).Value = l2d[ix-1][iy]

	def autofilter(self, on_off_tf=True):
		"""
		선택 영역에 자동 필터를 적용하거나 제거합니다.

		:param on_off_tf: True면 필터 적용, False면 제거
		:return: None

		Examples
		--------
		.. code-block:: python
        excel.select_range("", "A1:D10")
        excel.autofilter(True)   # 필터 적용
        excel.autofilter(False)  # 필터 제거
		"""
		if on_off_tf:
			self.range_obj.AutoFilter(on_off_tf)
		else:
			self.range_obj.Columns.AutoFilter()

	def autofilter_for_range(self, sheet_name, xyxy):
		"""
		선택한 영역에 자동필터를 적용하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.autofilter_for_range(sheet_name="", xyxy="")
			<object_name>.autofilter_for_range("sht1", [1,1,3,20])
			<object_name>.autofilter_for_range("", "")
		"""
		range_obj = self.new_range_obj(sheet_name, xyxy)
		range_obj.AutoFilter(1)

	def autofilter_for_range_with_by_criteria(self, sheet_name, xyxy, y_line=3, operator="or", input_value1="123", input_value2="있음"):
		"""
		선택한 영역안의 자동필터를 실행과 입력값으로 필터링하기

		Field : 설정이되는 Autofilter에서 적용을 원하는 열의 번호 (no)
		Criteria1 : 걸러내고자하는 기준값1, 다음과 같은 특수값 허용( "=" 값이 공백인 경우, "<>" 값이 공백이 아닌 경우, "><" (No Data)생략될 경우, 모든 데이터를 선택하는 것과 같다.
		Operator : 열겨형 XlAutoFilterOperaotr에 자세히 설명
		Criteria2 : 걸러내고자하는 기준값2
		VisibleDropDown : 제목 필드에 세모 버튼을 표기할지 유무

		xlAnd : 1, Criteria1 과 Criteria2에 대한논리적 AND 연산 결과
		xlOr : 2, Criteria1 과 Criteria2에 대한논리적 OR 연산 결과
		xlTop10Items : 3, 상위 10 개 아이템
		xlBottom10Items : 4, 하위 10 개 아이템
		xlTop10Percent : 5, 상위 10 퍼센트
		xlBottom10Percent : 6, 하위 10 퍼센트
		xlFilterValues : 7, 값에 대한 필터
		xlFilterCellColor : 8, 셀의 색깔에 대한 필터
		xlFilterFontColor : 9, 글자색에 대한 필터
		xlFilterIcon : 10, 아이콘에 대한 필터
		xlFilterDynamic : 11, 다이나믹 필터

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.autofilter_for_range_with_by_criteria(sheet_name="", xyxy="", y_line=3, operator= "or", input_value1="123", input_value2="있음")
			<object_name>.autofilter_for_range_with_by_criteria("", "", 3,  "or", "123", "있음")
			<object_name>.autofilter_for_range_with_by_criteria(sheet_name="sht1", xyxy=[1,1,3,4], y_line=3, operator= "or", input_value1="123", input_value2="있음")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Columns.AutoFilter(1)
		input_dic = {"Field": y_line}

		not_empty = ["not empty", "있음"]
		empty = ["empty", "비었음", "없음", ""]

		if operator == "and":
			input_dic["Criteria1"] = input_value1
			input_dic["Criteria2"] = input_value2
			input_dic["Operator"] = 1

		elif operator == "or":
			input_dic["Criteria1"] = input_value1
			input_dic["Criteria2"] = input_value2
			input_dic["Operator"] = 2

		elif operator == "top10":
			input_dic["Operator"] = 3

		elif operator == "bottom10":
			input_dic["Operator"] = 4

		elif operator == "top10%":
			input_dic["Operator"] = 5

		elif operator == "bottom10%":
			input_dic["Operator"] = 6

		elif operator == "value" or operator == "":
			input_dic["Operator"] = 7

			if input_value1 in empty:
				input_value1 = "="
			elif input_value1 in not_empty:
				input_value1 = "<>"
			input_dic["Criteria1"] = input_value1

		elif operator == "cell_color":
			input_dic["Operator"] = 8
			if isinstance(input_value1, list):
				input_value1 = self.color.change_rgb_to_rgbint(input_value1)
			input_dic["Criteria1"] = input_value1

		elif operator == "font_color":
			input_dic["Operator"] = 9
			if isinstance(input_value1, list):
				input_value1 = self.color.change_rgb_to_rgbint(input_value1)
			input_dic["Criteria1"] = input_value1
		elif operator == "icon":
			operator = 10
		elif operator == "dynamic":
			operator = 11

		range_obj.AutoFilter(**input_dic)

	def autofilter_off(self):
		"""
		선택 영역의 자동 필터를 제거합니다.

		:return: None

		Examples
		--------
		.. code-block:: python
		    excel.select_range("", "A1:D10")
		    excel.autofilter_off()
		"""
		self.autofilter(False)

	def autofilter_off_for_range(self, sheet_name, xyxy):
		"""
		선택한 영역안의 자동필터를 실행하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.autofilter_off_for_range(sheet_name="", xyxy="")
			<object_name>.autofilter_off_for_range("sht1", [1,1,3,20])
			<object_name>.autofilter_off_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Columns.AutoFilter()

	def autofilter_with_by_criteria(self, y_line, operator, input_value1, input_value2):
		"""
		선택 영역에 조건부 자동 필터를 적용합니다.

		:param y_line: 필터를 적용할 열 번호
		:param operator: 연산자 ("and", "or", "between", "equal", "greater" 등)
		:param input_value1: 첫 번째 조건 값
		:param input_value2: 두 번째 조건 값 (and/or/between 연산자에서 사용)
		:return: None

		Examples
		--------
		.. code-block:: python
		    excel.select_range("", "A1:D100")
		    excel.autofilter_with_by_criteria(3, "and", 100, 200)
		"""
		self.range_obj.Columns.AutoFilter(1)
		input_dic = {"Field": y_line}

		not_empty = ["not empty", "있음"]
		empty = ["empty", "비었음", "없음", ""]

		if operator == "and":
			input_dic["Criteria1"] = input_value1
			input_dic["Criteria2"] = input_value2
			input_dic["Operator"] = 1

		elif operator == "or":
			input_dic["Criteria1"] = input_value1
			input_dic["Criteria2"] = input_value2
			input_dic["Operator"] = 2

		elif operator == "top10":
			input_dic["Operator"] = 3

		elif operator == "bottom10":
			input_dic["Operator"] = 4

		elif operator == "top10%":
			input_dic["Operator"] = 5

		elif operator == "bottom10%":
			input_dic["Operator"] = 6

		elif operator == "value" or operator == "":
			input_dic["Operator"] = 7

			if input_value1 in empty:
				input_value1 = "="
			elif input_value1 in not_empty:
				input_value1 = "<>"
			input_dic["Criteria1"] = input_value1

		elif operator == "cell_color":
			input_dic["Operator"] = 8
			if isinstance(input_value1, list):
				input_value1 = self.color.change_rgb_to_rgbint(input_value1)
			input_dic["Criteria1"] = input_value1

		elif operator == "font_color":
			input_dic["Operator"] = 9
			if isinstance(input_value1, list):
				input_value1 = self.color.change_rgb_to_rgbint(input_value1)
			input_dic["Criteria1"] = input_value1
		elif operator == "icon":
			operator = 10
		elif operator == "dynamic":
			operator = 11

		self.range_obj.AutoFilter(**input_dic)

	def calc_angle_by_pxyxy(self, px1, py1, px2, py2):
		"""
		두개의 픽셀좌표값을 이용해서 각도를 계산하는 것

		:param px1: (int) 정수, 시작점의 x좌표의 픽셀
		:param py1: (int) 정수, 시작점의 y좌표의 픽셀
		:param px2: (int) 정수, 끝점의 x좌표의 픽셀
		:param py2: (int) 정수, 끝점의 y좌표의 픽셀
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.calc_angle_by_pxyxy(12,23,67,345)
		"""
		angle_radians = math.atan2((px2 - px1), (py2 - py1))
		angle_degrees = math.degrees(angle_radians)
		if angle_degrees == 0:
			angle_degrees += 360
		return angle_degrees

	def calc_cxy_by_angle_n_length_from_old_cxy(self, px, py, angle_degree, length):
		"""
		시작점을 기준으로 각도와 길이를 주면 좌표를 구해 주는것
		가로를 0으로하고, 왼쪽으로 360 도까지 가는 좌표를 구하는것

		:param px: (int) 정수 x좌표의 픽셀
		:param py: (int) 정수 y좌표의 픽셀
		:param angle_degree: (int) 정수 각도
		:param length: (int) 길이를 나타내는 정수
		:return: (list)
		Examples
		--------
		.. code-block:: python
			<object_name>.calc_cxy_by_angle_n_length_from_old_cxy(12, 23, 30, 345)
		"""
		angle_radian = math.radians(angle_degree)
		px2 = px + length * math.sin(angle_radian)
		py2 = py - length * math.cos(angle_radian)
		return [px2, py2]

	def change_56color_to_rgbint(self, input_56color):
		"""
		엑셀 기본 56색 팔레트 인덱스를 RGB 정수값으로 변환합니다.

		:param input_56color: 엑셀 56색 인덱스 (1-56)
		:return: RGB 정수값

		Examples
		--------
		.. code-block:: python
        rgb_int = excel.change_56color_to_rgbint(12)
        # 결과: 특정 RGB 정수값 (예: 255)
		"""
		rgb = self.change_56color_to_rgb(input_56color)
		result = self.color.change_rgb_to_rgbint(rgb)
		return result

	def change_alpha_to_int(self, input_value):
		"""
		엑셀 열 주소 문자(A, B, AA 등)를 숫자로 변환합니다.

		:param input_value: 열 주소 문자 (예: "A", "B", "AA")
		:return: 열 번호 (1부터 시작)

		Examples
		--------
		.. code-block:: python
        col_num = excel.change_alpha_to_int("A")   # 1
        col_num = excel.change_alpha_to_int("AA")  # 27
		"""
		result = 0
		for num in range(len(input_value)):
			result = result + (string.ascii_lowercase.index(input_value[num]) + 1) * (26 ** num)
		return result

	def change_any_address_to_xyxy(self, xyxy):
		"""
		입력으로 들어오는 여러형태의 주소값을 확인하는 것

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_any_address_to_xyxy(xyxy="")
			<object_name>.change_any_address_to_xyxy([1,1,3,20])
			<object_name>.change_any_address_to_xyxy([1,1,1,20])
		"""

		if type(xyxy) == type(self.xlapp.Selection):  # range객체가 들어왔을때 적용하기 위한것
			xyxy = xyxy.Address
		elif xyxy == "" or xyxy == None:  # 아무것도 입력하지 않을때
			xyxy = self.xlapp.Selection.Address

		if xyxy == [0, 0] or xyxy == [0, 0, 0, 0]:
			result = [1, 0, 1048576, 0]

		elif isinstance(xyxy, str):  # 문자열일때
			if "!" in xyxy:
				xyxy = xyxy.replace("=", "").split("!")[1]
			try:
				result = self.change_string_address_to_xyxy(xyxy)
			except:
				# 혹시 문자열이 이름영역일 경우
				sheet_obj = self.check_sheet_name("")
				temp = sheet_obj.Range(xyxy).Address
				result = self.change_string_address_to_xyxy(temp)

		elif isinstance(xyxy, list):  # 리스트형태 일때
			if len(xyxy) == 2:
				xyxy = xyxy + xyxy

			result = []
			for one in xyxy:
				if isinstance(one, str):  # 문자열일때
					if "!" in one:
						one = one.replace("=", "").split("!")[1]
					temp = self.change_char_to_num(one)
					result.append(temp)
				elif isinstance(one, int):
					result.append(one)

		if len(result) == 2:
			result = result + result
		try:
			changed_result = [min(result[0], result[2]),
							  min(result[1], result[3]),
							  max(result[0], result[2]),
							  max(result[1], result[3])]
		except:
			changed_result = result

		return changed_result

	def change_any_address_to_xyxy_3_sets(self, xyxy):
		"""
		어떤 형식의 주소 형태를 3가지 형태의 주소형태로 바꿔주는 것
		입력주소와 자료를 받아서 최소로할것인지 최대로 할것인지를 골라서 나타낼려고 만든것

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: [["$A$2:$B$3"],["A1","B2],[2,1,3,2]]무조건 3개의 형태로 나오도록 만든다
		Examples
		--------
		.. code-block:: python
			<object_name>.change_any_address_to_xyxy_3_sets(xyxy="")
			<object_name>.change_any_address_to_xyxy_3_sets([1,1,3,20])
			<object_name>.change_any_address_to_xyxy_3_sets([1,1,1,20])
		"""
		xyxy = self.change_xy_list_to_list(xyxy)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		result = {}
		x_len = len(xyxy)
		y_len = len(xyxy[0])

		y_len_rng = y2 - y1 + 1
		x_len_rng = x2 - x1 + 1

		max_num = max(map(lambda y: len(y), xyxy))
		min_num = min(map(lambda y: len(y), xyxy))

		max_y = max(y_len, y_len_rng)
		max_x = max(max_num, x_len_rng)
		min_y = max(y_len, y_len_rng)
		min_x = max(x_len, x_len_rng)

		# 입력할것중 가장 적은것을 기준으로 적용
		result["xyxy_min"] = [x1, y1, x1 + min_y, y1 + min_num]
		# 입력할것중 가장 큰것을 기준으로 적용
		result["xyxy_max"] = [x1, y1, x1 + max_y, y1 + max_y]
		# 일반적인기준으로 적용하는것
		result["xyxy_basic"] = [x1, y1, x1 + x_len, y1 + max_num]
		return result

	def change_any_address_to_xyxy_new(self, xyxy):
		#속도가 빠르게 만든것
		if xyxy in ["", None, "selection"]:
			self.get_address_for_selection()
			return
		elif isinstance(xyxy, str):
			return self.change_string_address_to_xyxy(xyxy)
		elif isinstance(xyxy, list):
			if xyxy == [0, 0] or xyxy == [0,0, 0, 0]:
				return [1, 0, 1048576, 0]
			if len(xyxy) == 2:
				xyxy = xyxy *2 # [1, 2] -> [1, 2, 1, 2]
				result= []
				try:
					for one in xyxy:
						if isinstance(one, int):
							result.append(one)
						elif isinstance(one, str):
							# 시트명 제거 ("Sheet1!A" -> "A")
							if "!" in one:
								one = one.split("!")[-1]
								# 등호 제거 및 문자를 숫자로 변환
							one = one.replace("=", "")
							result.append(self.change_char_to_num(one))
						# x1, y1, x2, y2 순서 정렬 (좌상단, 우하단 좌표로 변환)
						return [min(result[0], result[2]),	min(result[1], result[3]),	max(result[0], result[2]),	max(result[1], result[3])]
				except Exception:
					return "error"

	def change_any_color_to_rgb(self, color_name):
		"""
		입력으로 들어오는 여러형태의 색을 나타내는 값을 RGB형식의 리스트형으로 바꾸기

		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: (list) RGB형식의 리스트형, [123,234,234]
		Examples
		--------
		.. code-block:: python
			<object_name>.change_any_color_to_rgb(123456)
			<object_name>.change_any_color_to_rgb('빨강56')
			<object_name>.change_any_color_to_rgb([22,34,35])
		"""
		result = False
		if isinstance(color_name, int):
			result = self.color.change_rgbint_to_rgb(color_name)
		elif isinstance(color_name, str):
			result = self.color.change_xcolor_to_rgb(color_name)
		elif isinstance(color_name, list):
			if color_name[0] > 100 or color_name[1] > 100 or color_name[2] > 100:
				# 리스트는 2가지 형태로 rgb나 hsv가 가능하니 100이상이 되면 hsv이니, 전부 100이하이면 hsv로 하도록 한다
				result = color_name
			else:
				result = self.color.change_hsl_to_rgb(color_name)
		return result

	def change_char_to_num(self, input_char):
		"""
		문자열 형식의 주소를 숫자로 바꿔주는 것
		예를들어 b를 2로 바꾸는것이다
		문자가 오던 숫자가 오던 숫자로 변경하는 것이다

		:param input_char: (str) 입력으로 들어오는 텍스트, 문자열 형식의 주소
		:return: (int) 정수
		Examples
		--------
		.. code-block:: python
			<object_name>.change_char_to_num('b')
			<object_name>.change_char_to_num('ab')
		"""
		aaa = re.compile("^[a-zA-Z]+$")  # 처음부터 끝가지 알파벳일때
		result_str = aaa.findall(str(input_char))

		bbb = re.compile("^[0-9]+$")  # 처음부터 끝가지 숫자일때
		result_num = bbb.findall(str(input_char))

		if result_str != []:
			no = 0
			result = 0
			for one in input_char.lower()[::-1]:
				num = string.ascii_lowercase.index(one) + 1
				result = result + 26 ** no * num
				no = no + 1
		elif result_num != []:
			result = int(input_char)
		else:
			result = "error"
		return result

	def change_client_cxy_to_screen_cxy(self, input_hwnd, client_rect):
		"""
		어떤 프로그램의 영역을 나타내는 방법중 하나로,
		클라이언트 좌표를 윈도우 좌표로 변환 하는것

		:param input_hwnd: (int) 핸들값, 클라이언트 프로그램의 핸들값
		:param client_rect: (list) 화면의 4각형을 나타내는 리스트형
		:return: (list)
		Examples
		--------
		.. code-block:: python
			<object_name>.change_client_cxy_to_screen_cxy(31067, [12,34,56,123])
		"""
		top_left = win32gui.ClientToScreen(input_hwnd, (client_rect[0], client_rect[1]))
		bottom_right = win32gui.ClientToScreen(input_hwnd, (client_rect[2], client_rect[3]))

		return [top_left, bottom_right]

	def change_date_value_for_input(self, data):
		"""
		입력 데이터의 차원을 유지하면서 튜플을 리스트로 변환하고
		날짜 형식을 문자열로 변환합니다.

		:param data: 단일 값, 1차원 리스트/튜플, 2차원 리스트/튜플
		:return: 입력과 같은 차원의 리스트 (날짜는 문자열로 변환)

		Examples
		--------
		.. code-block:: python
        result = excel.change_date_value_for_input(10)
        result = excel.change_date_value_for_input([1, 2, 3])
        result = excel.change_date_value_for_input(datetime.datetime(2024, 1, 1))
		"""

	def change_eng_to_int(self, input_value):
		return self.change_char_to_num(input_value)

	def change_file_type(self, path, filename, original_type="EUC-KR", new_type="UTF-8", input_filename="D:\\temp\\abc.xlsx"):
		"""
		입력으로 들어오는 화일의 encoding type을 변경하는 것
		예를 들어 "EUC-KR"의 형식의 화일을 "UTF-8"형식으로 바꾸고 싶을때 사용하는것
		가끔 기본적인 어떤 프로그램에서 encoding type이 맞지 않아 다른것으로 변경이 필요할때 사용하는 것

		:param path: (str) 입력으로 들어오는 텍스트, 경로를 나타내는 것
		:param filename: (str) 화일의 이름을 나타내는 문자열
		:param original_type: (str) 입력으로 들어오는 텍스트, 입력으로 들어오는 파일의 인코딩 타입
		:param new_type: (str) 입력으로 들어오는 텍스트, 바꾸고 싶은 파일의 인코딩 타입
		:param input_filename: (str) 화일의 이름을 나타내는 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_file_type(path="d:\\temp", filename="filename1", original_type="EUC-KR", new_type="UTF-8", input_filename="D:\\temp\\abc.xlsx")
			<object_name>.change_file_type("d:\\temp", "filename1", "EUC-KR", "UTF-8", "D:\\temp\\abc.xlsx")
			<object_name>.change_file_type(path="d:\\temp1", filename="filename1", original_type="EUC-KR", new_type="UTF-8", input_filename="D:\\temp\\abc.xlsx")
		"""
		full_path = path + "\\" + filename
		full_path_changed = path + "\\" + input_filename + filename
		try:
			aaa = open(full_path, 'rb')
			result = chardet.detect(aaa.read())
			aaa.close()

			if result['encoding'] == original_type:
				aaa = open(full_path, "r", encoding=original_type)
				file_read = aaa.readlines()
				aaa.close()

				new_file = open(full_path_changed, mode='w', encoding=new_type)
				for one in file_read:
					new_file.write(one)
				new_file.close()
		except:
			print("화일이 읽히지 않아요=====>", filename)

	def change_num_to_char(self, input_no):
		"""
		영역주소를 변경하기 위해서 숫자를 문자로 바꿔주는 것
		사용법 : 2 -> b

		:param input_no: (int) 정수
		:return: (str)
		Examples
		--------
		.. code-block:: python
			<object_name>.change_num_to_char(12)
			<object_name>.change_num_to_char(23)
		"""
		re_com = re.compile(r"([0-9]+)")
		result_num = re_com.match(str(input_no))

		if result_num:
			base_number = int(input_no)
			result_01 = ''
			result = []
			while base_number > 0:
				div = base_number // 26
				mod = base_number % 26
				if mod == 0:
					mod = 26
					div = div - 1
				base_number = div
				result.append(mod)
			for one_data in result:
				result_01 = string.ascii_lowercase[one_data - 1] + result_01
			final_result = result_01
		else:
			final_result = input_no
		return final_result

	def change_num_to_currency(self, input_no):
		"""
		입력 숫자를 통화 단위로 만드는 것

		:param input_no: (int) 정수, 입력으로 들어오는 숫자
		:return: (str)
		Examples
		--------
		.. code-block:: python
			<object_name>.change_num_to_currency(1200000)
			<object_name>.change_num_to_currency(3500)
		"""
		units = ["", "십", "백", "천"]
		large_units = ["", "만", "억", "조", "경"]
		result = []

		if input_no == 0:
			return "영"

		for i in range(len(large_units)):
			part = input_no % 10000
			if part > 0:
				part_str = ""
				for j in range(len(units)):
					digit = part % 10
					if digit > 0:
						part_str = str(digit) + units[j] + part_str
					part //= 10
				result.insert(0, part_str + large_units[i])
			input_no //= 10000

		return "".join(result)

	def change_number_value_to_string(self, sheet_name, xyxy):
		"""
		입력한 영역의 값들을 소문자로 바꾸는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_value_as_lower(sheet_name="", xyxy="")
			<object_name>.change_value_as_lower("sht1", [1,1,3,20])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		for x, y in product(range(x1, x2 + 1), range(y1, y2 + 1)):
			one_value = sheet_obj.Cells(x, y).Value
			if isinstance(one_value, int):
				sheet_obj.Cells(x, y).Value = str(one_value)

	def change_pxyxy_to_pxywh(self, input_pxywh=""):
		"""
		2점의 픽셀좌표를 시작점의 픽셀을 기준으로 다음의 픽셀을 넓이와 높이(w, h)로 변경하는 것

		:param input_pxywh: (list) [영역중 왼쪽위의 x축의 픽셀번호, 영역중 왼쪽위의 y축의 픽셀번호, 넓이를 픽셀로 계산한것, 높이를 픽셀로 계산한것]
		:return: (list)
		Examples
		--------
		.. code-block:: python
			<object_name>.change_pxyxy2_pxywh([11,22,234,345])
		"""
		px1, py1, pw, ph = input_pxywh
		return [px1, py1, px1+pw, py1+ph]

	def change_range_n_ylist_to_dic(self, sheet_name, xyxy, y_list):
		"""
		** 왜 만들었는지 이젠 기억이 안남
		가로열로 넣을수있도록 영역의 자료를

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_y_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_range_n_ylist_to_dic("", "", [1,3,15,27])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		l2d = self.read_value_for_range(sheet_name, xyxy)
		result_xy = {}
		result = {}

		for index, l1d in enumerate(l2d):
			temp = ""
			for sero in y_list:
				temp = temp + str(l1d[sero - 1]) + "_"  # 세로의 자료들을 _로 다 연결한다
				temp = temp[:-1]
				if not temp in result.keys():
					result[temp] = [list(l1d)]
					result_xy[temp] = [[x1 + index, y1, x1 + index, y2]]
				else:
					result[temp].append([x1 + index, y1, x1 + index, y2])
		return [result, result_xy]

	def change_range_name_to_address(self, range_name):
		"""
		입력값을로 들어오는 이름영역의 주소를 갖고오는 것
		단, 이름영역의 주소형태는 시트이름 또한 포함이 되어있어서, 시트이름과 주소의 2개로 결과값을 돌려준다

		:param range_name: (str) 입력으로 들어오는 텍스트, 영역이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_range_name_to_address(range_name="영역이름1")
			<object_name>.change_range_name_to_address(sheet_name="", xyxy=[1,1,1,20])
			<object_name>.change_range_name_to_address("영역이름123")
		"""
		temp = self.get_address_for_range_name(range_name)
		xyxy = self.change_any_address_to_xyxy(temp[2])
		return xyxy

	def sheet2_name(self, sheet_name1, sheet_name2):
		"""
		시트이름 바꾸기

		:param sheet_name1: (str) 입력으로 들어오는 텍스트, 변경전 시트이름
		:param sheet_name2: (str) 입력으로 들어오는 텍스트, 변경후 시트이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.sheet2_name("sheet_name1", "sheet_name2")
		"""
		sheets_name = self.get_sheet_names()
		if not sheet_name2 in sheets_name:
			self.xlbook.Worksheets(sheet_name1).Name = sheet_name2

	def change_string_address_to_xyxy(self, xyxy):
		"""
		입력된 주소값을 [x1, y1, x2, y2]의 형태로 만들어 주는 것이다

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: (list), [x1, y1, x2, y2]의 형태
		Examples
		--------
		.. code-block:: python
			<object_name>.change_string_address_to_xyxy("$1:$8")
		"""
		aaa = re.compile("[a-zA-Z]+|\\d+")
		address_list = aaa.findall(str(xyxy))
		temp = []
		result = []

		for one in address_list:
			temp.append(self.util.check_one_address(one))

		if len(temp) == 1 and temp[0][1] == "string":  # "a"일때
			result = [0, temp[0][0], 0, temp[0][0]]
		elif len(temp) == 1 and temp[0][1] == "num":  # 1일때
			result = [temp[0][0], 0, temp[0][0], 0]
		elif len(temp) == 2 and temp[0][1] == temp[1][1] and temp[0][1] == "string":  # "a:b"일때
			result = [0, temp[0][0], 0, temp[1][0]]
		elif len(temp) == 2 and temp[0][1] == temp[1][1] and temp[0][1] == "num":  # "2:3"일때
			result = [temp[0][0], 0, temp[1][0], 0]
		elif len(temp) == 2 and temp[0][1] != temp[1][1] and temp[0][1] == "num":  # "2a"일때
			result = [temp[0][0], temp[1][0], temp[0][0], temp[1][0]]
		elif len(temp) == 2 and temp[0][1] != temp[1][1] and temp[0][1] == "string":  # "a2"일때
			result = [temp[1][0], temp[0][0], temp[1][0], temp[0][0]]
		elif len(temp) == 4 and temp[0][1] != temp[1][1] and temp[0][1] == "num":  # "a2b3"일때
			result = [temp[0][0], temp[1][0], temp[2][0], temp[3][0]]
		elif len(temp) == 4 and temp[0][1] != temp[1][1] and temp[0][1] == "string":  # "2a3c"일때
			result = [temp[1][0], temp[0][0], temp[3][0], temp[2][0]]
		return result

	def change_value_by_xsql(self, sheet_name, xyxy, iy, input_xre, input_value):
		"""
		선택한 영역의 한줄을 기준으로, 각 셀의 값을 input_xre로 찾아서 찾은값을 변경하는 것
		정규표현식을 이용하여 바꾸는 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param iy: (int) 정수
		:param input_xre: (str) xre형식의 문자열
		:param input_value: (str) 입력으로 들어오는 텍스트, 바꾸기 전의 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_value_by_xsql(sheet_name="", xyxy="", iy=5, input_xre="[시작:처음][영어:1~4][한글:3~10]", input_value="입력값2")
			<object_name>.change_value_by_xsql("", "", 7, "[시작:처음][영어:1~4][한글:3~10]", "입력값2")
			<object_name>.change_value_by_xsql(sheet_name="sht1", xyxy="", iy=5, input_xre="[시작:처음][영어:1~4][한글:3~10]", input_value="입력값2")
		"""
		l2d = self.read_value_for_range(sheet_name, xyxy)
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		for index, l1d in enumerate(l2d):
			try:
				aa = self.rex.replace_with_xsql(input_xre, input_value, l1d[iy])
				if aa != l1d[index]:
					sheet_obj.Cells(x1 + index, y1 + iy).Value = aa
			except:
				pass

	def change_value_for_range_as_capital(self, sheet_name, xyxy):
		"""
		입력한 영역의 값들의 첫글자만 대문자로 바꾸는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_value_for_range_as_capital(sheet_name="", xyxy="")
			<object_name>.change_value_for_range_as_capital("sht1", [1,1,3,20])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x, y in product(range(x1, x2 + 1), range(y1, y2 + 1)):
			one_value = sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				sheet_obj.Cells(x, y).Value = one_value.capitalize()

	def change_value_for_range_as_lower(self, sheet_name, xyxy):
		"""
		입력한 영역의 값들을 소문자로 바꾸는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_value_for_range_as_lower(sheet_name="", xyxy="")
			<object_name>.change_value_for_range_as_lower("sht1", [1,1,3,20])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x, y in product(range(x1, x2 + 1), range(y1, y2 + 1)):
			one_value = sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				sheet_obj.Cells(x, y).Value = one_value.lower()

	def change_value_for_range_as_ltrim(self, sheet_name, xyxy):
		"""
		입력영역의 값들의 왼쪽에 있는 공백을 삭제하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_value_for_range_as_ltrim(sheet_name="", xyxy="")
			<object_name>.change_value_for_range_as_ltrim("sht1", [1,1,3,20])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x, y in product(range(x1, x2 + 1), range(y1, y2 + 1)):
			one_value = sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				sheet_obj.Cells(x, y).Value = one_value.lstrip()

	def change_value_for_range_as_rtrim(self, sheet_name, xyxy):
		"""
		입력영역의 값들의 오른쪽에 있는 공백을 삭제하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_value_for_range_as_rtrim(sheet_name="", xyxy="")
			<object_name>.change_value_for_range_as_rtrim("sht1", [1,1,3,20])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x, y in product(range(x1, x2 + 1), range(y1, y2 + 1)):
			one_value = sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				sheet_obj.Cells(x, y).Value = one_value.rstrip()

	def change_value_for_range_as_swapcase(self, sheet_name, xyxy):
		"""
		입력영역의 값들의 대소문자를 바꾸는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_value_for_range_as_swapcase(sheet_name="", xyxy="")
			<object_name>.change_value_for_range_as_swapcase("sht1", [1,1,3,20])
			<object_name>.change_value_for_range_as_swapcase("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x, y in product(range(x1, x2 + 1), range(y1, y2 + 1)):
			one_value = sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				sheet_obj.Cells(x, y).Value = one_value.swapcase()

	def change_value_for_range_as_trim(self, sheet_name, xyxy):
		"""
		입력영역의 값들의 앞뒤 공백을 삭제하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_value_for_range_as_trim(sheet_name="", xyxy="")
			<object_name>.change_value_for_range_as_trim("sht1", [1,1,3,20])
			<object_name>.change_value_for_range_as_trim("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x, y in product(range(x1, x2 + 1), range(y1, y2 + 1)):
			one_value = sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				sheet_obj.Cells(x, y).Value = one_value.strip()

	def change_value_for_range_as_upper(self, sheet_name, xyxy):
		"""
		입력영역의 값들을 대문자로 바꾸는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_value_for_range_as_upper(sheet_name="", xyxy="")
			<object_name>.change_value_for_range_as_upper("sht1", [1,1,3,20])
			<object_name>.change_value_for_range_as_upper("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x, y in product(range(x1, x2 + 1), range(y1, y2 + 1)):
			one_value = sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				sheet_obj.Cells(x, y).Value = one_value.upper()

	def change_value_for_range_by_xsql(self, sheet_name, xyxy, iy, input_xre, input_value):
		"""
		선택한 영역의 한줄을 기준으로, 각 셀의 값을 input_xre로 찾아서 찾은값을 변경하는 것
		정규표현식을 이용하여 바꾸는 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param iy: (int) 정수
		:param input_xre: (str) xre형식의 문자열
		:param input_value: (str) 입력으로 들어오는 텍스트, 바꾸기 전의 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_value_for_range_by_xsql(sheet_name="", xyxy="", iy=5, input_xre="[시작:처음][영어:1~4][한글:3~10]", input_value="입력값2")
			<object_name>.change_value_for_range_by_xsql("", "", 7, "[시작:처음][영어:1~4][한글:3~10]", "입력값2")
			<object_name>.change_value_for_range_by_xsql(sheet_name="sht1", xyxy="", iy=5, input_xre="[시작:처음][영어:1~4][한글:3~10]", input_value="입력값2")
		"""
		l2d = self.read_value_for_range(sheet_name, xyxy)
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for index, l1d in enumerate(l2d):
			try:
				aa = self.rex.replace_with_xsql(input_xre, input_value, l1d[iy])
				if aa != l1d[index]:
					sheet_obj.Cells(x1 + index, y1 + iy).Value = aa
			except:
				pass

	def change_xy_list_to_address_char(self, xy_list):
		"""
		xy형식의 자료 묶음을 a1형식의 값으로 바꾸는 것

		:param xy_list: (list) 리스트형식의 셀의 주소가 들어가있는 2차원 리스트형식의 자료, [[1, 1], [2, 3], [2, 4]]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_xy_list_to_address_char(xy_list=[[1, 1], [2, 2]])
			<object_name>.change_xy_list_to_address_char([[1, 1], [2, 2]])
			<object_name>.change_xy_list_to_address_char(xy_list=[[2,3], [7,10]])
		"""
		xy_list = self.change_xy_list_to_list(xy_list)
		result = ""
		for one_data in xy_list:
			y_char = self.change_num_to_char(one_data[1])
			result = result + str(y_char[0]) + str(one_data[0]) + ', '
		return result[:-2]

	def change_xy_list_to_list(self, xy_list):
		"""
		입력으로 들어오는 자료형태가 xy_list인지를 확인하는 것

		:param xy_list: (list)
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_xy_list_to_list(xy_list=[[1, 1], [2, 2]])
			<object_name>.change_xy_list_to_list([[1, 1], [2, 2]])
			<object_name>.change_xy_list_to_list(xy_list=[[2,3], [7,10]])
		"""
		if type(xy_list) == type(xy_list):
			temp = []
			for one_value in xy_list:
				if type(one_value) == type(xy_list):
					temp.append(list(one_value))
				else:
					temp.append(one_value)
			return temp

		else:
			return xy_list

	def change_xy_to_a1(self, xy=""):
		"""
		입력으로 들어온 주소인 xy의 형태([1,2])를 A1형식으로 바꾸는 것

		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_xy_to_a1("", [1,1])
			<object_name>.change_xy_to_a1("", [7,20])
		"""
		x_char = self.change_num_to_char(xy[0])
		result = str(x_char[0]) + str(xy[1])
		return result

	def change_xylist_to_list(self, xy_list):
		"""
		입력으로 들어오는 자료형태가 xy_list인지를 확인하는 것

		:param xy_list: (list)
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.change_xylist_to_list(xy_list=[[1, 1], [2, 2]])
			<object_name>.change_xylist_to_list([[1, 1], [2, 2]])
			<object_name>.change_xylist_to_list(xy_list=[[2,3], [7,10]])
		"""
		self.change_xy_list_to_list(xy_list)

	def xyxy2_by_lrtb(self, xyxy="", left=10, right=10, top=30, bottom=70):
		"""
		입력으로 들어오는 영역에서 특정한 영역을 추출하거나 변경하는것
		x : +는 오른쪽으로 확장, - 는 왼쪽으로 이동, 0은 한줄만 남기고 나머지는 없애기

		만약 왼쪽 2줄만 남기고 싶다면, 아래와같이 2번 하면 된다
		[xyxy, 0, "","",""]
		[xyxy, 2, "","",""]

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param left: (int) 영역의 왼쪽끝을 나타내는 숫자
		:param right: (int) 영역의 오른쪽끝을 나타내는 숫자
		:param top: (int) 영역의 위쪽끝을 나타내는 숫자
		:param bottom: (int) 영역의 아래쪽끝을 나타내는 숫자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.xyxy2_by_lrtb(xyxy="", left=10, right=10, top=30, bottom=70)
			<object_name>.xyxy2_by_lrtb("", 10, 10, 30, 70)
			<object_name>.xyxy2_by_lrtb(xyxy=[1,1,5,7], left=10, right=10, top=30, bottom=70)
		"""
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		if left == 0:
			y1 = y2
		elif left == "":
			pass
		else:
			y1 = y1 + left

		if right == 0:
			y2 = y1
		elif right == "":
			pass
		else:
			y2 = y2 + right

		if top == "":
			pass
		elif top == 0:
			x1 = x2
		else:
			x1 = x1 + top

		if bottom == "":
			pass
		elif bottom == 0:
			x2 = x1
		else:
			x2 = x2 + bottom

		return [x1, y1, x2, y2]

	def xyxy2_to_dic_by_1st_value_is_key(self, xyxy):
		"""
		영역의 자료를 사전 형식으로 변경을 하는 것인데, 맨앞의 자료를 key로 하고 그 나머지를
		사전의 value로 나타내서 만드는 것
		어떤 자료를 맨앞의 번호를 기준으로 불러오고 싶을때 사용하기 위한 것

		주소록의 각 자료를 찾는 방법으로, 고유한 이름을 기준으로 ID를 리스트로 저장하는 것이다
		제일앞의 것이 id이다

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.xyxy2_to_dic_by_1st_value_is_key(xyxy=[2, 2, 18, 7])
			<object_name>.xyxy2_to_dic_by_1st_value_is_key([1,1,3,20])
			<object_name>.xyxy2_to_dic_by_1st_value_is_key([1,1,1,20])
		"""
		l2d = self.read_value_for_range("", xyxy)
		result = {}
		for l1d in l2d:
			for no in range(len(l1d), 0, -1):
				if l1d[no - 1]:
					if l1d[no - 1] in result.keys():
						result[l1d[no - 1]].append(l1d[0])
					else:
						result[l1d[no - 1]] = [l1d[0]]
					break
		return result

	def xyxy2_to_json_file(self, sheet_name, xyxy, input_filename, is_title_tf=False):
		"""
		엑셀자료를 json으로 만들기 (단, 엑셀자료의 첫줄은 제목이있어야한다)
		만약, 없는 option을 선택하면 1번부터 숫자로 만들어 진다
		이 제목이 key로 사용된다
		결과 : [json화일, 제목리스트]

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_filename: (str) 화일의 이름을 나타내는 문자열
		:param is_title_tf: (str) 제일윗줄이 제목을 나타내는 것인지를 확인하는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.xyxy2_to_json_file(sheet_name="", xyxy="", input_filename="D:\\my_file.xlsx", is_title_tf=False)
			<object_name>.xyxy2_to_json_file("", "", "D:\\my_file.xlsx", False)
			<object_name>.xyxy2_to_json_file("sht1", "", "D:\\my_file2.xlsx", is_title_tf=False)
		"""
		title_n_l2d = self.read_value_for_range(sheet_name, xyxy)
		if is_title_tf:
			title_list = []
			for index, value in enumerate(title_n_l2d[0]):
				title_list.append(str(index + 1))
			data_l2d = title_n_l2d
		else:
			title_list = title_n_l2d[0]
			data_l2d = title_n_l2d[1:]

		json_code = self.change_l2d_n_title_list_to_json_file(data_l2d, title_list)

		# 텍스트 파일로 저장
		if input_filename:
			with open(input_filename, "w", encoding="utf-8") as file:
				file.write(json_code)
		return [json_code, title_list, input_filename]

	def xyxy2_to_pxywh(self, sheet_name, xyxy):
		"""
		입력영역의 크기를 픽셀의 주소와 넓이 높이로 바꾸는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.xyxy2_to_pxywh(sheet_name="", xyxy="")
			<object_name>.xyxy2_to_pxywh("sht1", [1,1,3,20])
			<object_name>.xyxy2_to_pxywh("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		return [range_obj.Left, range_obj.Top, range_obj.Width, range_obj.Height]

	def xyxy2_to_pxyxy(self, xyxy):
		"""
		셀의 번호를 주면, 셀의 왼쪽과 오른쪽아래의 픽셀 주소를 돌려준다
		픽샐의 값으로 돌려주는것

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.xyxy2_to_pxyxy(xyxy="")
			<object_name>.xyxy2_to_pxyxy([1,1,3,20])
			<object_name>.xyxy2_to_pxyxy([1,1,1,20])
		"""
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		px1, py1, px1_w, py1_h = self.read_coord_for_cell("", [x1, y1])
		px2, py2, px2_w, py2_h = self.read_coord_for_cell("", [x2, y2])

		return [px1, py1, px2 + px2_w - px1, py2 + py2_h - py1]

	def xyxy2_to_r1c1(self, xyxy):
		"""
		입력으로 들어오는 [1,2,3,4] 를 "b1:d3"로 변경하는 것

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.xyxy2_to_r1c1("")
			<object_name>.xyxy2_to_r1c1([1,1,3,20])
		"""
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		str_1 = self.change_num_to_char(y1)
		str_2 = self.change_num_to_char(y2)
		if str(x1) == "0": x1 = ""
		if str(x2) == "0": x2 = ""
		if str_1 == "0": str_1 = ""
		if str_2 == "0": str_2 = ""

		return str_1 + str(x1) + ":" + str_2 + str(x2)

	def xyxy2_to_r1r1(self, xyxy):
		"""
		[1,2,3,4]형태의 자료를 "b1:b1"의 형태로 변경하는 것

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.xyxy2_to_r1r1("")
			<object_name>.xyxy2_to_r1r1([1,1,1,20])
		"""
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		str_1 = self.change_num_to_char(y1)
		return str_1 + str(x1) + ":" + str_1 + str(x1)

	def chart_bgcolor(self, input_chart_obj, chart_area_bg, plot_area_bg):
		"""
		차트의 배경색을 칠하는 것

		:param input_chart_obj: (object) 객체,
		:param chart_area_bg: (str) 챠트영역의 색을 나타내는 것
		:param plot_area_bg: (str) 플로트영역의 색을 나타내는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.chart_bgcolor(input_chart_obj="object1", chart_area_bg="", plot_area_bg="")
			<object_name>.chart_bgcolor("object1", "", "")
			<object_name>.chart_bgcolor(input_chart_obj="object7", chart_area_bg="", plot_area_bg="")
		"""
		input_chart_obj.ChartArea.Format.Fill.Visible = False
		input_chart_obj.PlotArea.Format.Fill.Visible = False

	def chart_gridline(self, input_chart_obj):
		"""
		차트의 그리드라인을 설정하는 것

		:param input_chart_obj: (object) 객체,
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_gridline_for_chart(input_chart_obj="chart1")
		"""
		input_chart_obj.Axes(2).MajorGridlines.Delete()
		input_chart_obj.Axes(2).MinorGridlines.Delete()

	def chart_legend(self, input_chart_obj, input_lrtb):
		"""
		차트의 범례에대한 속성을 설정

		:param input_chart_obj: (object) 객체, 챠트객체
		:param input_lrtb: (list) [왼쪽셀번호, 오른쪽셀번호, 위쪽셀번호, 아래쪽 셀번호]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_legend_for_chart(input_chart_obj="chart1", input_lrtb="top")
			<object_name>.set_legend_for_chart("chart1", "top")
		"""
		lrtb_dic = {"left": 103, "right": 101, "top": 102, "bottom": 104}
		input_chart_obj.SetElement(lrtb_dic[input_lrtb])

	def chart_style(self, input_chart_obj, chart_style):
		"""
		그래프의 형태를 정하는 것입니다

		:param input_chart_obj: (object) 객체, 차트객체
		:param chart_style: (str) 차트의 스타일을 나타내는 문자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_chart_style(input_chart_obj="object1",style="style1")
			<object_name>.set_chart_style("object1", "style1")
			<object_name>.set_chart_style(input_chart_obj="object1", style="style1")
		"""
		chart_style_vs_enum = {"line": 4, "pie": 5}
		checked_chart_no = chart_style_vs_enum[chart_style]
		input_chart_obj.ChartType = checked_chart_no
		return input_chart_obj

	def chart_x_scale(self, input_chart_obj, min_scale="", max_scale=""):
		"""
		차트의 속성을 설정 : x_scale

		:param input_chart_obj: (object) 객체, 차트객체
		:param min_scale: (int) 차트의 x스케일을 나타내는 최소 숫자
		:param max_scale: (int) 차트의 x스케일을 나타내는 최대 숫자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_x_scale_for_chart(input_chart_obj="object1", min_scale=20, max_scale=100)
			<object_name>.set_x_scale_for_chart("object1", 30, 100)
			<object_name>.set_x_scale_for_chart(input_chart_obj="object3", min_scale=40, max_scale=100)
		"""
		temp = input_chart_obj.Axes(1)
		temp.MinimumScale = min_scale
		temp.MaximumScale = max_scale

	def chart_x_title(self, input_chart_obj, xtitle="", input_size=12, color_name="", is_bold_tf=True):
		"""
		차트의 속성을 설정 : x_title

		:param input_chart_obj: (object) 객체, 차트객체
		:param xtitle: (str) 입력으로 들어오는 텍스트, 제목을 나타내는 문자열
		:param input_size: (int) 정수 크기를 나타내는 숫자
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56, 색을 나타내는 문자
		:param is_bold_tf: (bool) 진하게를 나타내는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_x_title_for_chart(chart_obj1, xtitle="제목1", input_size=12, color_name="red45", is_bold_tf=True)
			<object_name>.set_x_title_for_chart(chart_obj2, xtitle="제목2", input_size=11, color_name="red45", is_bold_tf=True])
			<object_name>.set_x_title_for_chart(chart_obj3, xtitle="제목3", input_size=12, color_name="red45", is_bold_tf=False)
		"""
		temp = input_chart_obj.Axes(1)  # 1 : xlCategory, 3 :xlSeriesAxis, 2 : xlValue, 1: primary, 2 : secondary
		temp.HasTitle = True
		temp.AxisTitle.Text = xtitle
		temp.AxisTitle.Format.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = self.color.change_xcolor_to_rgbint(color_name)
		temp.AxisTitle.Format.TextFrame2.TextRange.Font.Bold = is_bold_tf
		temp.AxisTitle.Format.TextFrame2.TextRange.Font.Size = input_size

	def chart_y_scale(self, input_chart_obj, min_scale="", max_scale=""):
		"""
		차트의 속성을 설정 : y_scale

		:param input_chart_obj: (object) 객체, 차트객체
		:param min_scale: (int) 차트의 y스케일을 나타내는 최소 숫자
		:param max_scale: (int) 차트의 y스케일을 나타내는 최대 숫자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_y_scale_for_chart(input_chart_obj=chart1, min_scale=5, max_scale=10)
			<object_name>.set_y_scale_for_chart(chart1, 5, 10)
			<object_name>.set_y_scale_for_chart(input_chart_obj=chart1, min_scale=15, max_scale=45)
		"""
		temp = input_chart_obj.Axes(2)
		temp.MinimumScale = min_scale
		temp.MaximumScale = max_scale

	def chart_y_title(self, input_chart_obj, xtitle="제목1", size="", color="", bold=""):
		"""
		차트의 속성을 설정 : y_title

		:param input_chart_obj: (object) 객체, 차트객체
		:param xtitle: (str) 입력으로 들어오는 텍스트, 제목을 나타내는 문자열
		:param size: (int) 정수 크기를 나타내는 숫자
		:param color: (str) 입력으로 들어오는 텍스트, 색을 나타내는 문자
		:param bold: (bool) 진하게를 나타내는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_y_title_for_chart(input_chart_obj="object1", xtitle="제목1", size=10, color="red23", bold=True)
			<object_name>.set_y_title_for_chart("object4", "제목1", 12, "red40", True)
			<object_name>.set_y_title_for_chart(input_chart_obj="object1", xtitle="제목1", size=11, color="red12", bold=False)
		"""
		temp = input_chart_obj.Axes(2)  # 1: xlCategory, 3 :xlSeriesAxis, 2 : xlValue, 1: primary, 2 : secondary
		temp.HasTitle = True
		temp.AxisTitle.Text = xtitle
		temp.AxisTitle.Format.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = self.color.change_xcolor_to_rgbint("red")
		temp.AxisTitle.Format.TextFrame2.TextRange.Font.Bold = True
		temp.AxisTitle.Format.TextFrame2.TextRange.Font.Size = 20

	def check_any_data_for_date(self, input_data):
		"""
		입력자료중 날짜 부분이 들어있는것을 text형태로 바꾸는 기능입니다
		날짜를 그대로 사용하면 에러가 나기 때문에 자료를 변경하는 것입니다
		:param input_data:
		:return:
		"""
		if isinstance(input_data, list) or isinstance(input_data, tuple):
			input_data = self.util.change_any_data_to_l2d(input_data)
		result = []
		for l1d in input_data:
			empty_list = []
			for value in l1d:
				# None 값 처리
				if value is None:
					empty_list.append(None)
				# 날짜/시간 타입 처리
				elif isinstance(value, (pywintypes.TimeType, datetime.datetime, datetime.date)):
					try:
						temp = str(value).split(" ")
						if len(temp) > 1 and temp[1] == "00:00:00+00:00":
							empty_list.append(temp[0])
						elif len(temp) > 1:
							aaa = temp[0] + " " + temp[1].split("+")[0]
							empty_list.append(aaa)
						else:
							# 날짜만 있는 경우
							empty_list.append(temp[0])
					except Exception as e:
						# 변환 실패 시 그냥 문자열로 변환
						empty_list.append(str(value))
				# 숫자, 문자열 등 일반 타입
				else:
					empty_list.append(value)
			result.append(empty_list)
		return result

	def check_basic_data(self, sheet_name, xyxy):
		"""
		자주 사용하는 것을 하나로 만들어서 관리하는것이 코드를 줄일것으로 보여서 만듦

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_basic_data(sheet_name="", xyxy="")
			<object_name>.check_basic_data("sht1", [1,1,3,20])
			<object_name>.check_basic_data("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		return [sheet_obj, range_obj, x1, y1, x2, y2]

	def check_cell_type(self, input_address):
		return self.check_string_address_style(input_address)

	def check_cell_value_is_startwith_input_value_and_move_cell_to_begin(self, startwith="*"):
		"""
		맨앞에 특정글자가 있으면, 앞으로 옮기기

		:param startwith: (str) 시작되는 문자열의 형식
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_cell_value_is_startwith_input_value_and_move_cell_to_begin(startwith="*")
			<object_name>.check_cell_value_is_startwith_input_value_and_move_cell_to_begin("*")
			<object_name>.check_cell_value_is_startwith_input_value_and_move_cell_to_begin("#")
		"""
		sheet_obj = self.check_sheet_name("")
		x, y, x2, y2 = self.get_address_for_selection()
		self.insert_yline("", y)
		for one_x in range(x, x2):
			one_value = self.read_value_for_cell("", [one_x, y + 1])
			if one_value.startswith(startwith):
				sheet_obj.Cells(one_x, y).Value = one_value
				sheet_obj.Cells(one_x, y + 1).Value = None

	def check_data_type_for_input_value(self, input_value):
		"""
		입력으로 들어온 값의 자료형이 str, int, real, boolen, list, tuple, dic인지를 알아내는 것

		:param input_value: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_data_type_for_input_value(123)
			<object_name>.check_data_type_for_input_value("abc")
			<object_name>.check_data_type_for_input_value([1,1,1,20])
		"""

		if isinstance(input_value, str):
			result = "str"
		elif isinstance(input_value, int):
			result = "int"
		elif isinstance(input_value, float):
			result = "real"
		elif isinstance(input_value, bool):
			result = "boolen"
		elif isinstance(input_value, list):
			result = "list"
		elif isinstance(input_value, tuple):
			result = "tuple"
		elif isinstance(input_value, dict):
			result = "dic"
		else:
			result = input_value
		return result

	def check_differ_at_2_same_area(self, sheet_name1, xyxy1, sheet_name2, xyxy2):
		"""
		동일한 사이즈의 다른 2개의 여역안의 값을 비교해서, 다른것이 발견되면 뒤에있는 영겨안의 셀의 색을 색칠하는 것

		:param sheet_name1: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy1: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param sheet_name2: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy2: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_differ_at_2_same_area(sheet_name1="", xyxy1="", sheet_name2="", xyxy2=[1,1,5,12])
			<object_name>.check_differ_at_2_same_area("sht1", "", "", [1,1,5,12])
			<object_name>.check_differ_at_2_same_area(sheet_name1="sht2", xyxy1=[1,1,3,5], sheet_name2="", xyxy2=[2,2,5,12])
		"""
		l2d_1 = self.read_value_for_range(sheet_name1, xyxy1)
		l2d_2 = self.read_value_for_range(sheet_name2, xyxy2)

		x11, y11, x12, y12 = self.change_any_address_to_xyxy(xyxy1)
		x21, y21, x22, y22 = self.change_any_address_to_xyxy(xyxy2)

		for x in range(len(l2d_1)):
			for y in range(len(l2d_1[0])):
				if l2d_1[x][y] != l2d_2[x][y]:
					self.paint_by_any_color_for_range(sheet_name1, [x + x11, y + y11], "yel")
					self.paint_by_any_color_for_range(sheet_name2, [x + x21, y + y21], "yel")

	def check_excel_filename(self, input_filename):
		"""
		입력으로 들어온 엑셀 화일이름을 적절하게 변경 시킨다

		:param input_filename: (str) 화일의 이름을 나타내는 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_excel_filename(input_filename="D:\\temp\\abc.xlsx")
			<object_name>.check_excel_filename("D:\\temp\\abc.xlsx")
			<object_name>.check_excel_filename("D:\\temp\\file.xlsx")
		"""
		if "\\" in input_filename or "/" in input_filename:
			pass
		else:
			path = self.get_current_path()
			input_filename = path + "\\" + input_filename

		input_filename = self.util.check_file_path(input_filename)

		if input_filename.endswith("xlsx") or input_filename.endswith("xls"):
			pass
		else:
			input_filename = input_filename + ".xlsx"

		return input_filename

	def check_excel_program(self):
		"""
		워크북이 하나도 없는 빈 엑셀 program만 실행중일때 엑셀 프로그램을 종료시키기 위한것
		즉, 빈 엑셀을 종료하는 목적이다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_excel_program()
		"""

		for proc in psutil.process_iter():
			if "excel" in str(proc.name()).lower():
				print(f"PID: {proc.pid}, Name: {proc.name()}")
				proc.kill()  # 프로세스 종료

	def check_file_in_folder(self, input_folder, input_filename):
		"""
		화일이 폴더안에 있는지를 확인하는 것

		:param input_folder: (str) 입력으로 들어오는 텍스트, 경로를 나타내는 것
		:param input_filename: (str) 화일의 이름을 나타내는 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_file_in_folder(input_folder="D:\\temp", input_filename="D:\\temp\\abc.xlsx")
			<object_name>.check_file_in_folder("D:\\temp", "D:\\temp\\abc.xlsx")
			<object_name>.check_file_in_folder("D:\\temp", input_filename="D:\\temp\\abc123.xlsx")
		"""
		result = False
		filenames = self.util.get_all_filename_in_folder(input_folder)
		if input_filename in filenames:
			result = True
		return result

	def check_file_path(self, input_filename):
		"""
		경로를 /와 \으로 사용하는 경우가 있어서, 그걸 변경하는 것

		:param input_filename: (str) 화일의 이름을 나타내는 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_file_path(input_filename="D:\\temp\\abc.xlsx")
			<object_name>.check_file_path("D:\\temp\\abc.xlsx")
			<object_name>.check_file_path("D:\\temp\\file.xlsx")
		"""
		changed_filename = str(input_filename).lower()
		changed_filename = changed_filename.replace("\\\\", "/")
		changed_filename = changed_filename.replace("\\", "/")
		return changed_filename

	def check_font_element(self, input_key):
		"""
		단어중 가장 가까운 단어들 찾기
		입력형식은 bold(),진하게(yes).. 이런식으로 입력이 되도록 하면 어떨까??

		:param input_key: (str) 입력으로 들어오는 텍스트,
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_font_element(input_key="key1")
			<object_name>.check_font_element("key1")
			<object_name>.check_font_element("key3")
		"""
		try:
			result = self.varx["check_font_para"][input_key]
		except:
			result = input_key
		return result

	def check_input_area(self, input_value):
		"""
		입력으로 들어오는 대부분의 주소형태를 xyxy형태로 만들어주는 것입니다
		:param input_value:
		:return:
		"""
		if isinstance(input_value[0], list):
			input_value = input_value[0]

		if len(input_value) == 1:
			x1 = self.change_char_to_num(input_value[0])
			return [x1]
		elif len(input_value) == 2:
			x1 = self.change_char_to_num(input_value[0])
			y1 = self.change_char_to_num(input_value[1])
			return [x1, y1]
		elif len(input_value) == 4:
			x1 = self.change_char_to_num(input_value[0])
			y1 = self.change_char_to_num(input_value[1])
			x2 = self.change_char_to_num(input_value[2])
			y2 = self.change_char_to_num(input_value[3])
			return [x1, y1, x2, y2]

	def check_input_data(self, input_value, none_is_none=False):
		"""
		입력 데이터를 표준화합니다.

		- None을 빈 문자열로 변환 (none_is_none=False일 때)
		- 튜플을 리스트로 변환
		- 날짜/시간 객체를 문자열로 변환
		- 중첩 구조 재귀적 처리

		:param input_value: 변환할 데이터
		:param none_is_none: True면 None을 유지, False면 빈 문자열로 변환
		:return: 표준화된 데이터

		Examples
		--------
		.. code-block:: python
        result = excel.check_input_data(None)           # ""
        result = excel.check_input_data(None, True)     # None
        result = excel.check_input_data((1, 2, 3))      # [1, 2, 3]
		"""
		if isinstance(input_value, (str, int, float, bool, dict, set)):
			return input_value
		if input_value is None:
			if none_is_none:
				return None
			else:
				return ""
		if isinstance(input_value, (tuple, list)):
			return [self.check_input_data(item) for item in input_value]
		if isinstance(input_value, (pywintypes.TimeType, datetime)):
			try:
				has_time = (hasattr(input_value, 'hour') and (input_value.hour != 0 or input_value.minute !=0 or input_value.second != 0))
				if has_time:
					return input_value.strftime('%Y-%m-%d %H:%M:%S')
				return input_value.strftime('%Y-%m-%d')
			except (AttributeError, ValueError, OSError):
				return str(input_value)
		return str(input_value)

	def check_input_list(self, input_list):
		"""
		입력을 1차원 리스트로 표준화합니다.

		- 문자열 → [문자열]
		- [[값들]] → [값들]

		:param input_list: 문자열, 리스트, 또는 2차원 리스트
		:return: 1차원 리스트

		Examples
		--------
		.. code-block:: python
        result = excel.check_input_list("text")      # ["text"]
        result = excel.check_input_list([1, 2, 3])   # [1, 2, 3]
        result = excel.check_input_list([[1, 2]])    # [1, 2]
		"""
		if isinstance(input_list, str):
			input_list = [input_list]
		elif isinstance(input_list[0], list):
			input_list = input_list[0]
		return input_list

	def check_input_values(self, input_value):
		"""
		보통의 어떤자료가 들어오면, 알아서 변수로 만들어 주는 것

		:param input_value: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_input_values(input_value="입력값")
			<object_name>.check_input_values("입력값")
		"""
		input_value = self.change_xy_list_to_list(input_value)
		result = {}

		if isinstance(input_value, dict):
			result.update(input_value)

		elif isinstance(input_value, list) and input_value != []:
			if isinstance(input_value[0], list):
				result["datas"] = input_value
			elif len(input_value) == 2 or len(input_value) == 4:
				try:
					result["xyxy"] = self.change_any_address_to_xyxy(input_value)
				except:
					pass

		elif isinstance(input_value, str):
			if "sheet" in input_value:
				result["sheet_name"] = input_value
			else:
				try:
					result["xyxy"] = self.change_any_address_to_xyxy(input_value)
				except:
					pass
		return result

	def check_item(self, xyxy, input_xre, changed_text):
		"""
		정규표현식의 약간 다른 ㅎ표현형식인 xre형식에 맞는 값을 입력값으로 바꾸는 것
		조건에 맞는 값을 변경하는 것

		:param xyxy2: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param input_xre: (str) xre형식의 문자열
		:param changed_text: (str) 입력으로 들어오는 텍스트,
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_item(xyxy="", input_xre="[시작:처음][영어:1~4][한글:3~10]", changed_text="")
			<object_name>.check_item("", "[시작:처음][영어:1~4][한글:3~10]", "")
			<object_name>.check_item(xyxy=[1,1,5,7], input_xre="[시작:처음][영어:1~4][한글:3~10]", changed_text="")
		"""

		resql = self.rex.change_xsql_to_resql(input_xre)
		x1, y1, x2, y2 = xyxy
		source_datas = self.read_value_for_range("", xyxy)
		for x in range(len(source_datas)):
			for y in range(len(source_datas[0])):
				one_source = source_datas[x][y]
				if one_source != None:
					source_datas[x][y] = re.sub(resql, one_source, changed_text)
		self.write_range("", [x1, y1], source_datas)
		return 1

	def check_line_style_as_dic(self, input_list):
		"""
		영역의 선의 형태를 적용할때, 일반적인 단어를 사용해도, 알아서 코드에서 사용하는 기본 용어로 바꿔주는 코드이다
		입력으로 들어오는 값에서 셀의 선에대한 속성들을 확인하는 것이다
		보통 선을 나타내는 속성은 선의위치, 선의 굵기, 선의 색, 선의형태을 리스트형식으로
		순서없이 입력을 해도, 적당한 형태로 바꿔주는 것
		결과값은 리스트형식으로 나타내는 것이다
		결과값 : {"color": "bla", "thickness": "", "line_style": "", "area": "box"}의 형태의 사전 형식

		:param input_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_line_style_as_dic(input_list=[1, "abc", "가나다"])
			<object_name>.check_line_style_as_dic([1, "abc", "가나다"])
			<object_name>.check_line_style_as_dic([1, "abc", "가나다"])
		"""

		result = {"color": "bla", "thickness": "", "line_style": "", "area": "box"}
		for one_value in input_list:
			if one_value in self.v_line_thickness_dic.keys():
				result["thickness"] = self.v_line_thickness_dic[one_value]
			elif one_value in self.v_line_style_dic.keys():
				result["style"] = self.v_line_style_dic[one_value]
			elif one_value in self.v_line_position.keys():
				result["area"] = self.v_line_position[one_value]
			elif self.color.check_color_name(one_value):
				try:
					result["color"] = self.color.change_xcolor_to_rgb(one_value)
				except:
					pass
		return result

	def check_list_address(self, input_list):
		"""
		주소값을 4자리 리스트로 만들기 위하여 사용하는것

		:param input_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_list_address(input_list=[1, "abc", "가나다"])
			<object_name>.check_list_address([1, "abc", "가나다"])
			<object_name>.check_list_address([1, "abc", "가나다"])
		"""
		input_list = self.check_input_data(input_list)

		result = []
		if len(input_list) == 1: # 값이 1개인경우 : ['1'], ['a']
			xy = str(input_list[0]).lower()
			if xy[0] in string.digits:
				result = [xy, 0, xy, 0]
			elif xy[0].lower() in string.ascii_lowercase:
				result = [0, xy, 0, xy]
		elif len(input_list) == 2: # 값이 2개인경우 : ['a', '1'], ['2', '3'], ['a', 'd']
			y1 = str(input_list[0]).lower()
			x1 = str(input_list[1]).lower()
			if y1[0] in string.digits:
				if x1[0] in string.digits:
					result = [y1, 0, x1, 0]
				elif x1[0] in string.ascii_lowercase:
					result = [y1, y1, y1, y1]
			elif y1[0] in string.ascii_lowercase:
				if x1[0] in string.digits:
					result = [x1, y1, y1, y1]
				elif x1[0] in string.ascii_lowercase:
					result = [0, y1, 0, x1]
		elif len(input_list) == 4: # 값이 4개인경우 : ['aa', '1', 'c', '44'], ['1', 'aa', '44', 'c']
			y1 = str(input_list[0]).lower()
			x1 = str(input_list[1]).lower()
			y2 = str(input_list[2]).lower()
			x2 = str(input_list[3]).lower()

			if y1[0] in string.digits and x2[0] in string.digits:
				if x1[0] in string.ascii_lowercase and x2[0] in string.ascii_lowercase:
					result = [x1, y1, x2, y2]
				elif x1[0] in string.digits and x2[0] in string.digits:
					result = [x1, y1, x2, y2]
			elif y1[0] in string.ascii_lowercase and x2[0] in string.ascii_lowercase:
				if x1[0] in string.digits and x2[0] in string.digits:
					result = [x1, y1, x2, x2]
		final_result = []
		for one in result:
			one_value = str(one)[0]
			if one_value in string.ascii_lowercase:
				aaa = self.change_char_to_num(one)
			else:
				aaa = str(one)
			final_result.append(aaa)
		return final_result

	def check_list_maxsize(self, input_l2d):
		"""
		2차원 배열안에있는 각 1차원의 리스트안의 갯수가 가장 큰것의 길이를 숫자로 나타내주는 것
		예: [[1,2,3],[4,5,6,5,6],[7,8,9]] => [4,5,6,5,6]의 갯수인 5를 돌려주는 것

		:param input_l2d: (list) 2차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_list_maxsize(input_l2d=[[1,2,3],[4,5,6,5,6],[7,8,9]])
			<object_name>.check_list_maxsize(input_l2d=[[1,2,3],[4,5,6,5,6],[7,8,9]])
			<object_name>.check_list_maxsize[[1,2,3],[4,5,6,5,6],[17,18,19]]
		"""
		input_l2d = self.check_input_data(input_l2d)
		return max(len(row) for row in input_l2d)

	def check_numberformat(self, sheet_name, xyxy):
		"""
		셀의 여러 값들을 가지고 셀값의 형태를 분석하는 것이다
		단, 속도가 좀 느려진다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_numberformat(sheet_name="", xyxy="")
			<object_name>.check_numberformat("sht1", [1,1,3,20])
			<object_name>.check_numberformat("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		result = []

		for x in range(x1, x2 + 1):
			temp = []
			for y in range(y1, y2 + 1):
				one_dic = {}
				one_cell = sheet_obj.Cells(x, y)
				one_dic["y"] = x
				one_dic["x"] = y
				one_dic["value"] = one_cell.Value
				one_dic["value2"] = one_cell.Value2
				one_dic["text"] = one_cell.Text
				one_dic["formula"] = one_cell.Formula
				one_dic["formular1c1"] = one_cell.FormulaR1C1
				one_dic["numberformat"] = one_cell.NumberFormat
				one_dic["type"] = type(one_cell.Value)

				if type(one_cell.Value) is pywintypes.TimeType:
					# pywintypes.datetime가 맞는지를 확인하는 코드이다
					print('날짜에요!', one_cell.Value, str(type(one_cell.Value)))

				tem_1 = ""
				if (
						"h" in one_cell.NumberFormat or "m" in one_cell.NumberFormat or "s" in one_cell.NumberFormat) and ":" in one_cell.NumberFormat:
					tem_1 = "time"

				if "y" in one_cell.NumberFormat or "mmm" in one_cell.NumberFormat or "d" in one_cell.NumberFormat:
					tem_1 = "date" + tem_1

				if isinstance(one_cell.Value, float) and one_cell.Value > 1 and tem_1 == "time":
					tem_1 = "datetime"

				one_dic["style"] = tem_1
				temp.append(one_dic)
			result.append(temp)
		return result

	def check_one_address(self, input_value):
		"""
		입력된 1개의 주소를 문자인지, 숫자인지 숫자로 변경하는 것이다

		:param input_value: (str) 입력으로 들어오는 텍스트
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_one_address(input_value="입력글자1")
			<object_name>.check_one_address("입력문자들")
			<object_name>.check_one_address("입력으로 들어오는 문자")
		"""
		re_com_1 = re.compile("^[a-zA-Z]+$")  # 처음부터 끝가지 알파벳일때
		result_str = re_com_1.findall(str(input_value))

		re_com_2 = re.compile("^[0-9]+$")  # 처음부터 끝가지 숫자일때
		result_num = re_com_2.findall(str(input_value))

		if result_num == [] and result_str != []:
			address_type = "string"
			no = 0
			address_int = 0
			for one in input_value.lower()[::-1]:
				num = string.ascii_lowercase.index(one) + 1
				address_int = address_int + 26 ** no * num
				no = no + 1
		elif result_str == [] and result_num != []:
			address_type = "num"
			address_int = int(input_value)
		else:
			address_int = "error"
			address_type = "error"
		return [address_int, address_type, input_value]

	def check_panthom_link_at_workbook(self):
		"""
		현재 활성화된 엑셀 화일안의 이름영역중에서 연결이 끊긴 것을 삭제하기위해 확인하는 것

		Examples
		--------
		.. code-block:: python
			<object_name>.check_panthom_link_at_workbook()
		"""
		names_count = self.xlbook.Names.Count
		result = []
		if names_count > 0:
			for aaa in range(1, names_count + 1):
				name_name = self.xlbook.Names(aaa).Name
				name_range = self.xlbook.Names(aaa)

				if "#ref!" in str(name_range).lower():
					print("found panthom link!!! ===> ", name_name)
					result = True
				else:
					print("normal link, ", name_name)
					result = False
		return result

	def check_password_for_sheet(self, num_tf="yes", text_small_tf="yes", text_big_tf="yes", special_tf="no", len_num=10):
		"""
		입력으로 들어온 시트의 암호를 찾아주는것

		:param num_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:param text_small_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:param text_big_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:param special_tf:(bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:param len_num: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_password_for_sheet(num_tf="yes", text_small_tf="yes", text_big_tf="yes", special_tf="no", len_num=10)
			<object_name>.check_password_for_sheet("yes", "yes", "yes", "no", 10)
			<object_name>.check_password_for_sheet(num_tf="yes", text_small_tf="no", text_big_tf="yes", special_tf="no", len_num=20)
		"""
		check_char = []
		if num_tf == "yes":
			check_char.extend(list(string.digits))
		if text_small_tf == "yes":
			check_char.extend(list(string.ascii_lowercase))
		if text_big_tf == "yes":
			check_char.extend(list(string.ascii_uppercase))
		if special_tf == "yes":
			for one in "!@#$%^*M-":
				check_char.extend(one)
		for no in range(1, len_num + 1):
			zz = itertools.combinations_with_replacement(check_char, no)
			for aa in zz:
				try:
					pswd = "".join(aa)
					self.set_sheet_lock_off("", pswd)
					return
				except:
					pass

	def check_password_style(self, num_tf, text_small_tf, text_big_tf, special_tf, len_num):
		"""
		암호에 걸린 화일을 열때 사용할 목적으로 만든것으로, 암호로 사용가능한 형태를 지정하는 것입니다

		:param num_tf:
		:param text_small_tf:
		:param text_big_tf:
		:param special_tf:
		:param len_num:
		:return:
		"""
		check_char = []
		if num_tf == "yes":
			check_char.extend(list(string.digits))
		if text_small_tf == "yes":
			check_char.extend(list(string.ascii_lowercase))
		if text_big_tf == "yes":
			check_char.extend(list(string.ascii_uppercase))
		if special_tf == "yes":
			for one in "!@#$%^*M-":
				check_char.extend(one)
		for no in range(1, len_num + 1):
			zz = itertools.combinations_with_replacement(check_char, no)
			for aa in zz:
				try:
					pswd = "".join(aa)
					self.unlock_sheet_by_password(pswd)
					return
				except:
					pass

	def check_price(self, input_no=3):
		"""
		1000단위로 숫자에 쉼표를 넣고, 밑에서부터 백만원단위, 천만원단위, 억단위로 바꾸는 것

		:param input_no: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_price(input_no=3)
			<object_name>.check_price(5)
			<object_name>.check_price(7)
		"""
		input_no = int(input_no)
		if input_no > 100000000:
			result = str('{:.If}'.format(input_no / 100000000)) + "억원"
		elif input_no > 10000000:
			result = str('{: .0f}'.format(input_no / 1000000)) + "백만원"
		elif input_no > 1000000:
			result = str('{:.If}'.format(input_no / 1000000)) + "백만원"
		return result


	def check_range_name(self, range_name="name1"):
		"""
		입력으로 들어온 이름역역이 있는지 확인하는 것

		:param range_name: (str) 입력으로 들어오는 텍스트,
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_range_name(range_name="영역이름1")
			<object_name>.check_range_name("영역이름1")
			<object_name>.check_range_name("영역이름123")
		"""
		all_range_name = self.get_range_names()
		result = False
		if not all_range_name:
			result = False
		else:
			if range_name in all_range_name:
				result = True
		return result

	def check_same_data(self, input_list, check_line):
		"""
		엑셀의 선택한 자료에서 여러줄을 기준으로 같은 자료만 갖고오기

		:param input_list: (list) 1차원의 list형 자료
		:param check_line: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_same_data(input_list=[1, "abc", "가나다"], check_line=10)
			<object_name>.check_same_data([1, "abc", "가나다"], 10)
			<object_name>.check_same_data(input_list=[1, "abc", "가나다"], check_line=12])
		"""
		input_list = self.check_input_data(input_list)
		result = []
		base_value = ""
		xy = self.get_address_for_activecell()
		for no in input_list:
			base_value = base_value + str(self.read_value_for_cell("", [xy[0], no]))

		# 혹시 1보다 작은 숫자가 나올 수있으므로, 최소시작점을 1로하기위해
		start_x = max(int(xy[0]) - check_line, 1)

		# 위로10개 아래로 10개의 자료를 확인한다
		for no in range(start_x, start_x + 20):
			one_value = ""
			for one in input_list:
				one_value = one_value + str(self.read_value_for_cell("", [no, one]))
			if base_value == one_value:
				# 보통 50개이상의 줄을 사용하지 않으므로 50개를 갖고온다
				temp = self.read_value_for_range("", [no, 1, no, 50])
				result.append(temp[0])
		return result

	def check_same_data_for_two_range(self, xyxy1, xyxy2):
		"""
		두개의 영역을 비교해서 같은것을 찾아내는 것

		앞의것이 기준 자료이며, 뒤의것이 찾을 대상이다

		1) 찾을 자료에서 같은것을 찾으면 그셀에 색칠을 하고
		2) 최종적으로 같은것은 새로운 시트에 써준다

		:param xyxy1: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param xyxy2: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_same_data_for_two_range(xyxy1=[1,1,30,30], xyxy2=[40,1, 70, 30])
			<object_name>.check_same_data_for_two_range([1,1,30,30], [40,1, 70, 30])
			<object_name>.check_same_data_for_two_range(xyxy1=[1,1,40,30], xyxy2=[40,1, 80, 30])
		"""
		sheet_obj = self.check_sheet_name("")
		base_l2d = self.read_value_for_range("", xyxy1)
		base_l1d = self.util.change_l2d_to_l1d(base_l2d)  # 비교를 위하여 1차원자료로 만든것
		same_data = []

		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy2)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = self.read_value_for_cell("", [x, y])
				if one_value:
					if one_value in base_l1d:
						same_data.append(one_value)
						sheet_obj.Cells(x, y).Interior.Color = self.color.change_xcolor_to_rgbint("red80")

		self.new_sheet()
		sheet_obj.Cells(1, 1).Value = "동일한 값입니다"
		self.write_l1d_from_cell_as_yline("", [1, 2], same_data)
		return 1

	def check_same_line_for_two_xyxy2_new_sheet(self, sheet_name, xyxy1, xyxy2):
		"""
		2개 영역에서 같은것을 찾아서 3가지로 나누어서 새로운 시트에 쓰는것

		- 1번 : 서로 같은것
		- 2번 : 앞의 자료중 다른 것
		- 2번 : 뒤의 자료중 다른 것
		영역을 나타내는 xyxy1또는 xyxy2 변수의 기본값을 ""일때는 현재 선택된 영역을 뜻하는 것입니다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy1: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param xyxy2: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_same_line_for_two_xyxy2_new_sheet(sheet_name="", xyxy1=[1,1,30,30], xyxy2=[40,1, 70, 30])
			<object_name>.check_same_line_for_two_xyxy2_new_sheet("", [1,1,30,30], [40,1, 70, 30])
			<object_name>.check_same_line_for_two_xyxy2_new_sheet(sheet_name="sht1", xyxy1=[1,1,30,30], xyxy2=[40,1, 70, 30])
		"""
		sheet_obj = self.check_sheet_name("")
		data1 = self.read_value_for_range(sheet_name, xyxy1)
		data2 = self.read_value_for_range(sheet_name, xyxy2)

		data1_found = []
		data1_not_found = []
		data2_not_found = []

		for one in data2:
			if not one in data1:
				data2_not_found.append(one)

		for one in data1:
			if one in data2:
				data1_found.append(one)
			else:
				data1_not_found.append(one)

		self.new_sheet()
		sheet_obj.Cells(1, 1).Value = "2 영역중 같은것"
		self.write_l2d_from_cell("", [2, 1], data1_found)

		line2_start = len(data1_found) + 5
		sheet_obj.Cells(line2_start - 1, 1).Value = "비교자료중 못찾은 것 (앞의 자료)"
		self.write_l2d_from_cell("", [line2_start, 1], data1_not_found)

		line3_start = line2_start + len(data1_not_found) + 5

		sheet_obj.Cells(line3_start - 1, 1).Value = "결과가 중요한 것중 못찾은 것 (뒷 자료)"
		self.write_l2d_from_cell("", [line3_start, 1], data2_not_found)

	def check_sheet_name(self, sheet_name):
		"""
		시트이름으로 객체를 만들어서 돌려주는 것이다

		이름이 없으면 현재 활성화된 시트를 객체로 만들어 사용한다
		숫자가 들어오면, 번호숫자로 생각해서 앞에서 n번째의 시트이름을 갖고과서 시트객체를 돌려준다
		#1 : 현재 워크북의 순번에 따른 시트객체를 갖고온다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_sheet_name(sheet_name="")
			<object_name>.check_sheet_name("sht1")
			<object_name>.check_sheet_name("")
		"""
		# 속도 빠르게 변경한것
		# None이거나 빈 문자열("")이이 바로 리턴 (가장 빠름)
		if sheet_name is None or sheet_name == "":
			return self.xlbook.ActiveSheet

		# 문자열 처리
		if isinstance(sheet_name, str):
			if sheet_name.lower() in ("activesheet", "active_sheet"):
				return self.xlbookActiveSheet
			return self.xlbook.Worksheets(sheet_name)

		# 숫자 처리 (엑셀 인덱스)
		if isinstance(sheet_name, int):
			return self.xlbook.Worksheets(sheet_name)

		# 그 1외 (기존 로직 유지)
		return self.xlbookActiveSheet

	def check_string_address(self, xyxy):
		"""
		string형태의 address를 문자와 숫자로 나누는것

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: 숫자와 문자로 된부분을 구분하는 것
		Examples
		--------
		.. code-block:: python
			<object_name>.check_string_address(xyxy="")
			<object_name>.check_string_address([1,1,3,20])
			<object_name>.check_string_address([1,1,1,20])
		"""
		aaa = re.compile("[a-zA-Z]+|\\d+")
		result = aaa.findall(str(xyxy))
		return result

	def check_string_address_style(self, xyxy):
		"""
		주소형태의 문자열이 어떤 형태인지 알아 내는 것

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능,주소형태의 문자열
		:return: "a1", "aa", "11"
		Examples
		--------
		.. code-block:: python
			<object_name>.check_string_address_style(xyxy="")
			<object_name>.check_string_address_style([1,1,3,20])
			<object_name>.check_string_address_style([1,1,1,20])
		"""
		result = ""
		if xyxy[0][0] in string.ascii_lowercase and xyxy[1][0] in string.digits:
			result = "a1"
		if xyxy[0][0] in string.ascii_lowercase and xyxy[1][0] in string.ascii_lowercase:
			result = "aa"
		if xyxy[0][0] in string.digits and xyxy[1][0] in string.digits:
			result = "11"
		return result

	def check_title_value(self, temp_title):
		"""
		화일의 제목으로 사용이 불가능한것을 제거한다

		:param temp_title:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_title_value(temp_title = "입력값")
			<object_name>.check_title_value("입력값")
			<object_name>.check_title_value("입력값123")
		"""
		for temp_01 in [[" ", "_"], ["(", "_"], [")", "_"], ["/", "_per_"], ["%", ""], ["'", ""], ['"', ""], ["$", ""],
						["__", "_"], ["__", "_"]]:
			temp_title = temp_title.replace(temp_01[0], temp_01[1])
		if temp_title[-1] == "_":
			temp_title = temp_title[:-2]
		return temp_title

	def check_xx_address(self, xyxy):
		"""
		입력 주소중 xx가 맞는 형식인지를 확인하는것

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: [2, 2]의 형태로 만들어 주는것
		Examples
		--------
		.. code-block:: python
			<object_name>.check_xx_address(xyxy="")
			<object_name>.check_xx_address([1,3])
			<object_name>.check_xx_address([1,20])
		"""
		if isinstance(xyxy, list):
			if len(xyxy) == 1:
				result = [xyxy[0], xyxy[0]]
			elif len(xyxy) == 2:
				result = xyxy
		else:
			x = self.change_char_to_num(xyxy)
			result = [x, x]
		return result

	def check_xy_address(self, xy):
		"""
		x나 y의 하나를 확인할때 입력을 잘못하는 경우를 방지하기위해 사용

		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: [3,3], [2,3], [4,4], [1,4]
		Examples
		--------
		.. code-block:: python
			<object_name>.check_xy_address(xyxy="")
			<object_name>.check_xy_address([1,1])
			<object_name>.check_xy_address([1,20])
		"""
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xy)
		return [x1, y1]

	def check_y_address(self, input_value):
		"""
		결과 = "b"의 형태로 만들어 주는것

		:param input_value: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.check_y_address(input_value = "입력값")
			<object_name>.check_y_address("입력값")
			<object_name>.check_y_address("입력값123")
		"""
		result = self.check_yy_address(input_value)[0]
		return result

	def check_yy_address(self, input_value):
		"""
		결과 = ["b", "b"]의 형태로 만들어 주는것

		:param input_value: (any) 입력값
		:return: ["b", "b"]의 형태로 만들어 주는것
		"""

		if input_value == "" or input_value == None:
			temp = self.get_address_for_selection()
			result = [temp[1], temp[3]]
		elif isinstance(input_value, str) or isinstance(input_value, int):
			temp = self.change_num_to_char(input_value)
			result = [temp, temp]
		elif isinstance(input_value, list):
			if len(input_value) == 2:
				result = input_value  # 이부분이 change_any_address_to_xyxy와 틀린것이다
			elif len(input_value) == 4:
				temp = input_value
				result = [temp[1], temp[3]]
		else:
			temp = self.get_address_for_selection()
			result = [temp[1], temp[3]]

		new_y1 = self.change_num_to_char(result[0])
		new_y2 = self.change_num_to_char(result[1])

		return [new_y1, new_y2]

	def close(self):
		"""
		열려진 엑셀 화일을 닫는것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.close()
		"""
		self.xlbook.Close(SaveChanges=0)
		del self.xlapp

	def close_active_workbook(self):
		"""
		열려진 엑셀 화일을 닫는것
		여러개가 있다면 활성화된 화일을 닫는다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.close_active_workbook()
		"""
		self.xlbook.Close(SaveChanges=0)

	def close_workbook(self, work_book_obj):
		"""
		열려진 엑셀 화일을 닫는것
		여러개가 있다면 활성화된 화일을 닫는다

		:param work_book_obj: (object) 객체,
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.close_workbook(work_book_obj=obj1)
			<object_name>.close_workbook(obj1)
			<object_name>.close_workbook(work_book_obj=obj123)
		"""
		work_book_obj.Close(SaveChanges=0)

	def conditional_format_by_cell_value(self, color_name, start_xy, input_value, cf_no):
		char_y = self.change_num_to_char(start_xy[1])

		if cf_no == None:
			cf_no = self.xlapp.Selection.FormatConditions.Count + 1

		self.range_obj.FormatConditions.Add(2, None, f'''=${char_y + str(start_xy[0])}={input_value}''', cf_no)
		self.range_obj.FormatConditions(cf_no).Interior.Color = self.color.change_xcolor_to_rgbint(color_name)

	def conditional_format_by_cell_value_for_range(self, sheet_name, xyxy, color_name="yel70", start_xy=[3, 5], input_value="입력값12", cf_no=None):
		"""
		선택한 영역의 n 번째 값이 입력값과 같으면, 전체 가로줄에 색칠하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:param start_xy: (list or str) 셀영역으로 [1,2], ''(현재 선택 영역)로 사용가능
		:param input_value: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.conditional_format_by_cell_value(sheet_name="", xyxy="", color_name="yel70", start_xy=[3,5], input_value="입력값12")
			<object_name>.conditional_format_by_cell_value("", "", "yel70", [3,5], "입력값12")
			<object_name>.conditional_format_by_cell_value(sheet_name="sht1", xyxy=[1,1,5,7], color_name="yel70", start_xy=[3,5], input_value="입력값12")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		char_y = self.change_num_to_char(start_xy[1])

		if cf_no == None:
			cf_no = self.xlapp.Selection.FormatConditions.Count +1

		range_obj.FormatConditions.Add(2, None, f'''=${char_y + str(start_xy[0])}={input_value}''', cf_no)
		range_obj.FormatConditions(cf_no).Interior.Color = self.color.change_xcolor_to_rgbint(color_name)

	def conditional_format_by_empty_value(self, input_value, color_name, start_xy, cf_no):
		"""
		조건부서식의 적용기준 : 기준셀의 값이 비어있을때 적용
		:param input_value:
		:param color_name:
		:param start_xy:
		:param cf_no:
		:return:
		"""
		char_y = self.change_num_to_char(start_xy[1])
		if cf_no == None:
			cf_no = self.xlapp.Selection.FormatConditions.Count + 1

		self.range_obj.FormatConditions.Add(2, None, f'''=${char_y + str(start_xy[0])}={input_value}''', cf_no)
		self.range_obj.FormatConditions(cf_no).Interior.Color = self.color.change_xcolor_to_rgbint(color_name)

	def conditional_format_by_empty_value_for_range(self, sheet_name, xyxy, color_name="yel70", start_xy=[3, 5], cf_no=None):
		"""
		선택한 영역의 n 번째 값이 비어있지 않으면, 전체 가로줄에 색칠하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:param start_xy: (list or str) 셀영역으로 [1,2], ''(현재 선택 영역)로 사용가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.conditional_format_by_empty_value(sheet_name="", xyxy="", color_name="yel70", start_xy=[3,5])
			<object_name>.conditional_format_by_empty_value("", "", "yel70", [3,5])
			<object_name>.conditional_format_by_empty_value(sheet_name="sht1", xyxy="", color_name="red45", start_xy=[3,5])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		char_y = self.change_num_to_char(start_xy[1])
		if cf_no == None:
			cf_no = self.xlapp.Selection.FormatConditions.Count +1

		range_obj.FormatConditions.Add(2, None, f'''=${char_y + str(start_xy[0])}=""''', cf_no)
		range_obj.FormatConditions(cf_no).Interior.Color = self.color.change_xcolor_to_rgbint(color_name)

	def conditional_format_by_function(self, input_formula, color_name, cf_no):
		"""
		조건부서식의 적용기준 : 기준셀에 함수를 넣어서, 그함수에 맞을때 적용됨

		:param input_formula:
		:param color_name:
		:param cf_no:
		:return:
		"""
		self.select()

		if cf_no == None:
			cf_no = self.xlapp.Selection.FormatConditions.Count + 1
		self.range_obj.FormatConditions.Add(2, None, input_formula, cf_no)
		self.range_obj.FormatConditions(cf_no).Interior.Color = self.color.change_xcolor_to_rgbint(color_name)

	def conditional_format_by_function_for_range(self, sheet_name, xyxy, input_formula="=LEN(TRIM($A1))=0", color_name="red50", cf_no=None):
		"""
		조건부서식 : 함수사용

		conditional_format_with_function("", [1, 1, 7, 7], "=LEN(TRIM($A1))=0")
		만약 형태를 바꾸고 싶으면 setup을 먼저 이용해서 형태를 설정합니다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_formula: (str) 수식을 나타내는 것
		:param range_format:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.conditional_format_by_function(sheet_name="", xyxy="", input_formula="=LEN(TRIM($A1))=0", range_format="red50")
			<object_name>.conditional_format_by_function("", "", "=LEN(TRIM($A1))=0", "red50")
			<object_name>.conditional_format_by_function(sheet_name="sht1", xyxy=[1,1,5,7], input_formula="=LEN(TRIM($A1))=0", range_format="red50")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		self.select_range(sheet_name, xyxy)

		if cf_no == None:
			cf_no = self.xlapp.Selection.FormatConditions.Count +1
		range_obj.FormatConditions.Add(2, None, input_formula, cf_no)
		range_obj.FormatConditions(cf_no).Interior.Color = self.color.change_xcolor_to_rgbint(color_name)

	def conditional_format_by_multi_operator(self, input_l2d):
		"""
		조건부서식의 적용기준 : 몇가지 서식이 사용가능하도록 만든것
		다중 조건부서식

		:param input_l2d:
		:return:
		"""
		for index, [operator, range_format] in enumerate(input_l2d):
			operator = str(operator).strip().upper()
			aaa = self.util.split_operator(operator)
			if operator.startswith("AND") or operator.startswith("OR"):
				# "and(100<=$A1, $A1<200)"	 "or(100<=$A1, $A1<200)" 등을 사용할때
				self.range_obj.FormatConditions.Add(2, None, "=" + operator)
			elif operator.startswith("="):
				# 보통 수식을 사용할때 적용되는 것
				self.range_obj.FormatConditions.Add(2, None, operator)
			elif not "," in operator and len(aaa) == 5:
				# "100<=$A31<200", between은 and 2개로 표현이 가능하다
				self.range_obj.FormatConditions.Add(2, None,
													"=AND(" + aaa[0] + aaa[1] + aaa[2] + "," + aaa[2] + aaa[3] + aaa[
														4] + ")")
			elif not "," in operator and len(aaa) == 3:
				# "100>$A10"
				self.range_obj.FormatConditions.Add(2, None, "=" + operator)

			if "color" in range_format.keys():
				self.range_obj.FormatConditions(index + 1).Interior.Color = self.color.change_xcolor_to_rgbint(
					range_format["color"])
			if "font_bold" in range_format.keys():
				self.range_obj.FormatConditions(index + 1).Font.Bold = True
			if "font_color" in range_format.keys():
				self.range_obj.FormatConditions(index + 1).Font.Color = self.color.change_xcolor_to_rgbint(
					range_format["font_color"])

	def conditional_format_by_multi_operator_for_range(self, sheet_name, xyxy, input_l2d):
		"""
		다중 조건부서식

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_l2d: (list) 2차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.conditional_format_by_multi_operator(sheet_name, xyxy, input_l2d)
			<object_name>.conditional_format_by_multi_operator("", "", [[1, 2], [4, 5]])
			<object_name>.conditional_format_by_multi_operator(sheet_name="sht1", xyxy="", input_l2d=[[1, 2], [4, 5]])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		for index, [operator, range_format] in enumerate(input_l2d):
			operator = str(operator).strip().upper()
			aaa = self.util.split_operator(operator)
			if operator.startswith("AND") or operator.startswith("OR"):
				# "and(100<=$A1, $A1<200)"	 "or(100<=$A1, $A1<200)" 등을 사용할때
				range_obj.FormatConditions.Add(2, None, "=" + operator)
			elif operator.startswith("="):
				# 보통 수식을 사용할때 적용되는 것
				range_obj.FormatConditions.Add(2, None, operator)
			elif not "," in operator and len(aaa) == 5:
				# "100<=$A31<200", between은 and 2개로 표현이 가능하다
				range_obj.FormatConditions.Add(2, None, "=AND(" + aaa[0] + aaa[1] + aaa[2] + "," + aaa[2] + aaa[3] + aaa[4] + ")")
			elif not "," in operator and len(aaa) == 3:
				# "100>$A10"
				range_obj.FormatConditions.Add(2, None, "=" + operator)

			if "color" in range_format.keys():
				range_obj.FormatConditions(index + 1).Interior.Color = self.color.change_xcolor_to_rgbint(range_format["color"])
			if "font_bold" in range_format.keys():
				range_obj.FormatConditions(index + 1).Font.Bold = True
			if "font_color" in range_format.keys():
				range_obj.FormatConditions(index + 1).Font.Color = self.color.change_xcolor_to_rgbint(range_format["font_color"])

	def conditional_format_by_not_none_value(self, input_value, color_name, start_xy, cf_no):
		"""
		조건부 서식을 적용하는 것 : 값이 있을때 적용되는 것이다
		:param input_value:
		:param color_name:
		:param start_xy:
		:param cf_no:
		:return:
		"""
		x11, y11, x22, y22 = self.change_any_address_to_xyxy(start_xy)
		char_y = self.change_num_to_char(self.y11)
		if cf_no == None:
			cf_no = self.xlapp.Selection.FormatConditions.Count + 1

		# self.range_obj.FormatConditions.Delete() # 영역에 포함된 조건부 서식을 지우는 것
		self.range_obj.FormatConditions.Add(2, None, f'''=${char_y + str(start_xy[0])}={input_value}''', cf_no)
		self.range_obj.FormatConditions(cf_no).Interior.Color = self.color.change_xcolor_to_rgbint(color_name)

	def conditional_format_by_not_none_value_for_range(self, sheet_name, xyxy, color_name="yel70", start_xy=[3, 5], cf_no=None):
		"""
		선택한 영역의 n 번째 값이 입력값과 같으면, 전체 가로줄에 색칠하기

		cf_no : 여러개의 conditional format을 사용할때 이용하기위하여, 번호를 넣는 것, cf를 몇번째 일지를 선택하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:param start_xy: (list or str) 셀영역으로 [1,2], ''(현재 선택 영역)로 사용가능
		:param cf_no: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.conditional_format_by_not_none_value(sheet_name="", xyxy="", color_name="yel70", start_xy=[3,5], cf_no=1)
			<object_name>.conditional_format_by_not_none_value("", [1,1,3,20], "yel70", [3,5], 1)
			<object_name>.conditional_format_by_not_none_value("sht1", [1,1,1,20], color_name="yel70", start_xy=[3,5], cf_no=1)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		x11, y11, x22, y22 = self.change_any_address_to_xyxy(start_xy)
		char_y = self.change_num_to_char(y11)
		if cf_no == None:
			cf_no = self.xlapp.Selection.FormatConditions.Count +1

		# range_obj.FormatConditions.Delete() # 영역에 포함된 조건부 서식을 지우는 것
		range_obj.FormatConditions.Add(2, None, f'''=${char_y + str(start_xy[0])}<>""''', cf_no)
		range_obj.FormatConditions(cf_no).Interior.Color = self.color.change_xcolor_to_rgbint(color_name)

	def conditional_format_by_operator(self, operator, range_format, type):
		type_dic = {"AboveAverageCondition": 12, "BlanksCondition": 10,
					"value": 1, "CellValue": 1, "ColorScale": 3, "DataBar": 4, "ErrorsCondition": 16,
					"Expression": 2, "IconSet": 6, "NoBlanksCondition": 13, "NoErrorsCondition": 17,
					"TextString": 9, "TimePeriod": 11, "Top10": 5, "Uniquevalues": 8, }
		oper_dic1 = {"between": 1, "equal": 3, "greater": 5, "greaterequal": 7, "less": 6, "Lessequal": 8,
					 "notbetween": 2, "notequal": 4,
					 "-": 3, ">": "<", ">=": "<=", "<": ">", "<=": ">=", "|-": 4}

		oper_dic2 = {"between": 1, "equal": 3, "greater": 5, "greaterequal": 7, "less": 6, "Lessequal": 8,
					 "notbetween": 2, "notequal": 4,
					 "-": 3, ">": 5, ">=": 7, "<": 6, "<=": 8, "|-": 4}

		r1c1 = self.xyxy2_to_r1c1('')
		cf_count = self.xlapp.Selection.FormatConditions.Count
		type_value = type_dic[type]

		if type_value == 1:  # 셀값을 기준으로 판단
			aaa = self.util.split_operator(operator)
			if len(aaa) == 5:
				self.range_obj.FormatConditions.Add(
					Type=2,
					Formula1=f'=AND({r1c1}{oper_dic1[aaa[1]]}{aaa[0]},{r1c1}{aaa[3]}{aaa[-1]})'
				)
				self.range_obj.FormatConditions(cf_count + 1).SetFirstPriority()
				self.range_obj.FormatConditions(cf_count + 1).Interior.Color = self.color.change_xcolor_to_rgbint(
					range_format)

			elif len(aaa) == 3:
				self.range_obj.FormatConditions.Add(
					Type=2,
					Formula1=f'=({r1c1}{oper_dic1[aaa[1]]}{aaa[0]})'
				)
				self.range_obj.FormatConditions(cf_count + 1).SetFirstPriority()
				self.range_obj.FormatConditions(cf_count + 1).Interior.Color = self.color.change_xcolor_to_rgbint(
					range_format)

	def conditional_format_by_operator_for_range(self, sheet_name, xyxy, operator="100<=value<200", range_format="red50", type="value"):
		"""
		조건부서식 사용하기

		conditional_format_with_operator("", [1, 1, 7, 7], "100<=value <200")

		만약 형태를 바꾸고 싶으면 setup을 먼저 이용해서 형태를 설정합니다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param type: (str) 조건부서식에서 사용하는 형태선택
		:param operator: (str) 캍거나 크고 작음을 나타내는 문자
		:param range_format:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.conditional_format_by_operator(sheet_name="", xyxy="", type="type1", operator="greater", range_format="red50")
			<object_name>.conditional_format_by_operator("", [1,1,3,20], type="type1", operator="greater", range_format="red50")
			<object_name>.conditional_format_by_operator("sht1", [1,1,1,20], type="type1", operator="greater", range_format="red50")
		"""
		type_dic = {"AboveAverageCondition": 12, "BlanksCondition": 10,
					"value": 1,"CellValue": 1, "ColorScale": 3, "DataBar": 4, "ErrorsCondition": 16,
					"Expression": 2, "IconSet": 6, "NoBlanksCondition": 13, "NoErrorsCondition": 17,
					"TextString": 9, "TimePeriod": 11, "Top10": 5, "Uniquevalues": 8, }
		oper_dic1 = {"between": 1, "equal": 3, "greater": 5, "greaterequal": 7, "less": 6, "Lessequal": 8,
					"notbetween": 2, "notequal": 4,
					"-": 3, ">": "<", ">=": "<=", "<": ">", "<=": ">=", "|-": 4}

		oper_dic2 = {"between": 1, "equal": 3, "greater": 5, "greaterequal": 7, "less": 6, "Lessequal": 8,
					"notbetween": 2, "notequal": 4,
					"-": 3, ">": 5, ">=": 7, "<": 6, "<=": 8, "|-": 4}

		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		r1c1 = self.xyxy2_to_r1c1(xyxy)
		cf_count = self.xlapp.Selection.FormatConditions.Count
		type_value = type_dic[type]

		if type_value == 1:  # 셀값을 기준으로 판단
			aaa = self.util.split_operator(operator)
			if len(aaa) == 5:
				range_obj.FormatConditions.Add(
					Type=2,
					Formula1=f'=AND({r1c1}{oper_dic1[aaa[1]]}{aaa[0]},{r1c1}{aaa[3]}{aaa[-1]})'
				)
				range_obj.FormatConditions(cf_count + 1).SetFirstPriority()
				range_obj.FormatConditions(cf_count + 1).Interior.Color = self.color.change_xcolor_to_rgbint(range_format)

			elif len(aaa) == 3:
				range_obj.FormatConditions.Add(
					Type=2,
					Formula1=f'=({r1c1}{oper_dic1[aaa[1]]}{aaa[0]})'
				)
				range_obj.FormatConditions(cf_count + 1).SetFirstPriority()
				range_obj.FormatConditions(cf_count + 1).Interior.Color = self.color.change_xcolor_to_rgbint(range_format)

	def conditional_format_for_3_colored_gradation_style(self, sheet_name, xyxy, color_name_top="yel70", color_name_middle="yel70", color_name_bottom=" red45"):
		"""
		그라데이션으로 색을 칠하는 것
		최고값의색, 중간값의 색, 최저값의 색을 정하면, 그 중간은 각각의 색들의 그라데이션으로 나타나는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name_top: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:param color_name_middle: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:param color_name_bottom: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.conditional_format_for_3_colored_gradation_style(sheet_name="", xyxy="", color_name_top="yel70", color_name_middle="yel70", color_name_bottom=" red45")
			<object_name>.conditional_format_for_3_colored_gradation_style("", [1,1,3,20], color_name_top="yel70", color_name_middle="yel70", color_name_bottom=" red45")
			<object_name>.conditional_format_for_3_colored_gradation_style("sht1", [1,1,1,20], color_name_top="yel70", color_name_middle="yel70", color_name_bottom=" red45")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		#range_obj.FormatConditions.Delete()
		range_obj.FormatConditions.AddColorScale(ColorScaleType=3)
		[csc1, csc2, csc3] = [range_obj.FormatConditions(1).ColorScaleCriteria(n) for n in range(1, 4)]

		csc1.Type = 1
		csc1.FormatColor.Color = self.color.change_xcolor_to_rgbint(color_name_bottom)
		csc1.FormatColor.TintAndShade = 0

		csc2.Type = 5
		csc2.FormatColor.Color = self.color.change_xcolor_to_rgbint(color_name_middle)
		csc2.FormatColor.TintAndShade = 0

		csc3.Type = 2
		csc3.FormatColor.Color = self.color.change_xcolor_to_rgbint(color_name_top)
		csc3.FormatColor.TintAndShade = 0

	def conditional_format_for_data_bar_style(self, sheet_name, xyxy, color_name):
		"""
		조건부서식 : 바타입
		만약 형태를 바꾸고 싶으면 setup을 먼저 이용해서 형태를 설정합니다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.conditional_format_for_data_bar_style(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.conditional_format_for_data_bar_style("sht1", [1,1,12,23], "red23")
			<object_name>.conditional_format_for_data_bar_style("", [3,3,5,7], "gra34")
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		ad = range_obj.FormatConditions.AddDatabar()
		ad.BarColor.Color = self.color.change_xcolor_to_rgbint(color_name)

	def conditional_format_for_set_format(self, input_range_obj, input_dic):
		"""
		조건부서식에서 셀의 셀서식을 정의하기위한 설정
		""나 "basic"으로 입력이 되어있으면 기본설정값으로 적용이 되는 것입니다
		사용법 : {"line_style":1, "line_color":"red", "line_color":"red", "font_bold":1, "line_color":"red", }
		:param input_range_obj: (object) 객체
		:param input_dic: (dic) 사전형으로 입력되는 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.conditional_format_for_set_format(input_range_obj="object1", input_dic = {"key1":1, "line_1":"red", "input_color":"red", "font_bold":1})
			<object_name>.conditional_format_for_set_format("object1", {"key1":1, "line_1":"red", "input_color":"red", "font_bold":1})
			<object_name>.conditional_format_for_set_format(input_range_obj="object3", input_dic = {"key1":1, "line_1":"red", "input_color":"red", "font_bold":1})
		"""
		if input_dic == "" or input_dic == "basic":
			input_range_obj.Borders.LineStyle = 1
			input_range_obj.Borders.ColorIndex = 1
			input_range_obj.Interior.Color = 5296274
			input_range_obj.Font.Bold = 1
			input_range_obj.Font.ColorIndex = 1
		else:
			if "line_style" in input_dic.keys():
				input_range_obj.Borders.LineStyle = input_dic["line_style"]
			if "line_color" in input_dic.keys():
				rgbint = self.color.change_xcolor_to_rgbint(input_dic["line_color"])
				input_range_obj.Borders.Color = rgbint
			if "color" in input_dic.keys():
				rgbint = self.color.change_xcolor_to_rgbint(input_dic["color"])
				input_range_obj.Interior.Color = rgbint
			if "font_bold" in input_dic.keys():
				input_range_obj.Font.Bold = input_dic["font_bold"]
			if "font_color" in input_dic.keys():
				rgbint = self.color.change_xcolor_to_rgbint(input_dic["font_color"])
				input_range_obj.Font.Color = rgbint

	def copy(self):
		"""
		현재 선택된 영역을 클립보드에 복사합니다.

		:return: None

		Examples
		--------
		.. code-block:: python
		    excel.select_range("", "A1:B10")
		    excel.copy()
		"""
		self.range_obj.Copy()

	def copy_and_paste(self, sheet1, sheet2, xyxy1, xyxy2):
		"""
		복사한후 붙여넣기

		:param sheet1: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param sheet2: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy1: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param xyxy2: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.copy_and_paste(sheet1="", sheet2="sht2", xyxy1=[1,1,12,12], xyxy2=[3,3,5,18])
			<object_name>.copy_and_paste("", "sht2", [1,1,12,12], [3,3,5,18])
			<object_name>.copy_and_paste(sheet1="sht1", sheet2="sht2", xyxy1=[3,3,12,12], xyxy2=[5,5,7,18])
		"""
		sheet_obj_1 = self.check_sheet_name(sheet1)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy1)
		range_obj = sheet_obj_1.Range(sheet_obj_1.Cells(x1, y1), sheet_obj_1.Cells(x2, y2))
		range_obj.Copy()

		x21, y21, x22, y22 = self.change_any_address_to_xyxy(xyxy2)
		self.select_sheet(sheet2)
		self.xlapp.ActiveSheet.Cells(x21, y22).Select()
		self.xlapp.ActiveSheet.Paste()

	def copy_function_from_xyxy1_to_xyxy2(self, sheet_name, xyxy1, xyxy2):
		"""
		xlSheet_to_final.Range("A53:A54").AutoFill(xlSheet_to_final.Range("A53:A61"),xlFillDefault)

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy1: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param xyxy2: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.copy_function_from_xyxy1_to_xyxy2(sheet_name="", xyxy1=[1,1,30,30], xyxy2=[40,1, 70, 30])
			<object_name>.copy_function_from_xyxy1_to_xyxy2("", [1,1,30,30], [40,1, 70, 30])
			<object_name>.copy_function_from_xyxy1_to_xyxy2(sheet_name="sht1", xyxy1=[1,1,30,30], xyxy2=[40,1, 70, 30])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy1)
		range_obj_1 = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy2)
		range_obj_2 = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		range_obj_1.AutoFill(range_obj_2)

	def copy_n_paste_as_value(self, sheet_name, xyxy):
		"""
		선택한 영역을 값으로 만들기위한 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.copy_n_paste_as_value(sheet_name="", xyxy="")
			<object_name>.copy_n_paste_as_value("sht1", [1,1,3,20])
			<object_name>.copy_n_paste_as_value("", "")
		"""
		# 사용된 영역 (데이터가 있는 영역) 파악
		range_obj = self.set_common_for_sheet_n_range_obj(sheet_name, xyxy)
		range_obj.Copy()  # 사용된 영역 복사
		range_obj.PasteSpecial(Paste=11)  # 값으로 붙여넣기 (xlPasteValues = 11)

	def copy_range(self, sheet_name, xyxy):
		"""
		영역의 복사까지만 하는 기능이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.copy_range(sheet_name="", xyxy="")
			<object_name>.copy_range("sht1", [1,1,3,20])
			<object_name>.copy_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		range_obj.Copy()

	def sheet1_at_same_workbook(self, sheet_name1, sheet_name2):
		"""
		같은 엑셀화일안에 있는 시트를 복사해서 하나더 만드는 것

		:param sheet_name1: (str) 입력으로 들어오는 텍스트, 복사할 전의 시트 이름
		:param sheet_name2: (str) 입력으로 들어오는 텍스트, 새로운 시트 이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.sheet1_at_same_workbook(sheet_name1="name1", sheet_name2="name2")
			<object_name>.sheet1_at_same_workbook("", "name2")
			<object_name>.sheet1_at_same_workbook("sht1", "name2")
		"""

		sheets_name = self.get_sheet_names()
		if sheet_name1 in sheets_name:
			sheet_obj = self.check_sheet_name(sheet_name1)

			sheet_obj.Copy(Before=sheet_obj)
			if not sheet_name2 == "":
				old_name = self.get_activesheet_name()
				self.sheet2_name(old_name, sheet_name2)
		else:
			print("Can not found sheet name")

	def sheet1_to_another_workbook(self, source_wb, source_sheet_name_l1d, target_position=1):
		"""
		어떤 엑셀화일안의 시트를 다른 엑셀화일에 복사하는 것

		:param source_wb: (object) 워크북의 객체
		:param source_sheet_name_l1d: 리스트형태가 아니면, 리스트로 만들어 준다
		:param target_position: 현재 엑셀의 몇번째 위치에 복사를 할것인지를 선택하는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.sheet1_to_another_workbook(source_wb=swb1, source_sheet_name_l1d=["sht1", "sht2"], target_position=1)
			<object_name>.sheet1_to_another_workbook(swb1, ["sht1", "sht2"], 3)
			<object_name>.sheet1_to_another_workbook(source_wb=swb3, source_sheet_name_l1d=["sht1", "sht2"], target_position=2)
		"""
		if not isinstance(source_sheet_name_l1d, list):
			source_sheet_name_l1d = [source_sheet_name_l1d]
		for one_sheet_name in source_sheet_name_l1d:
			sheet_obj = self.check_sheet_name(one_sheet_name)
			sheet_obj.Copy(Before=source_wb.xlbook.Sheets(target_position))

	def copy_value_for_range_to_another_sheet(self, sheet_name1, xyxy1, sheet_name2, xyxy2):
		"""
		특정 영역을 복사해서 다른시트의 영역에 붙여 넣기

		:param sheet_name1: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy1: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param sheet_name2: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy2: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.copy_value_for_range_to_another_sheet(sheet_name1="", xyxy1="", sheet_name2="", xyxy2=[1,1,5,12])
			<object_name>.copy_value_for_range_to_another_sheet("sht1", "", "", [1,1,5,12])
			<object_name>.copy_value_for_range_to_another_sheet(sheet_name1="sht2", xyxy1=[1,1,3,5], sheet_name2="", xyxy2=[2,2,5,12])
		"""

		sheet_obj1 = self.check_sheet_name(sheet_name1)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy1)
		range_obj1 = sheet_obj1.Range(sheet_obj1.Cells(x1, y1), sheet_obj1.Cells(x2, y2))
		range_obj1.Select()

		sheet_obj2 = self.check_sheet_name(sheet_name2)
		x11, y11, x21, y21 = self.change_any_address_to_xyxy(xyxy2)
		range_obj2 = sheet_obj2.Range(sheet_obj2.Cells(x11, y11), sheet_obj2.Cells(x21, y21))
		range_obj2.Paste()

		self.xlapp.CutCopyMode = 0

	def copy_xxline(self, sheet_name, xyxy):
		"""
		가로영역을 복사

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.copy_xxline(sheet_name="", xyxy="")
			<object_name>.copy_xxline("sht1", [1,1,3,20])
			<object_name>.copy_xxline("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, x2 = self.check_xx_address(xyxy)
		sheet_obj.Rows(str(x1) + ":" + str(x2)).Copy()

	def copy_yyline(self, sheet_name, xyxy):
		"""
		세로영역을 복사

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.copy_yyline(sheet_name="", xyxy="")
			<object_name>.copy_yyline("sht1", [1,1,3,20])
			<object_name>.copy_yyline("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_yy_address(xyxy)
		sheet_obj.Columns(str(y1) + ":" + str(y2)).Copy()

	def count_conditional_format_for_sheet(self, sheet_name):
		return self.count_conditional_format_for_sheet(sheet_name)

	def count_continuous_same_value(self):
		total = 0
		for y in range(self.y2, self.y1, -1):
			for x in range(self.x1, self.x2 + 1):
				base_value = self.read_value_for_cell("", [x, y])
				up_value = self.read_value_for_cell("", [y - 1, x])
				if base_value == up_value:
					total = total + 1
		return total

	def count_continuous_same_value_for_range(self, sheet_name, xyxy):
		"""
		선택한 영역중 세로로 연속된 같은자료만 개수세기
		밑에서부터 올라가면서 찾는다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.count_continuous_same_value_for_range(sheet_name="", xyxy="")
			<object_name>.count_continuous_same_value_for_range("sht1", [1,1,3,20])
			<object_name>.count_continuous_same_value_for_range("", "")
		"""
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		total = 0
		for y in range(y2, y1, -1):
			for x in range(x1, x2 + 1):
				base_value = self.read_cell_value(sheet_name, [x, y])
				up_value = self.read_cell_value(sheet_name, [y - 1, x])
				if base_value == up_value:
					total = total + 1
		return total

	def count_empty_cell(self):
		temp_result = 0
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = self.read_value_for_cell("", [x, y])
			if one_value == None:
				self.sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint(16)
				temp_result = temp_result + 1
		return temp_result

	def count_empty_cell_for_range(self, sheet_name, xyxy):
		"""
		영역안의 빈셀의 갯수를 계산
		빈셀의 의미 : None인것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.count_empty_cell_for_range(sheet_name="", xyxy="")
			<object_name>.count_empty_cell_for_range("sht1", [1,1,3,20])
			<object_name>.count_empty_cell_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		temp_result = 0
		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				one_value = self.read_value_for_cell(sheet_name, [x, y])
				if one_value == None:
					sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint(16)
					temp_result = temp_result + 1
		return temp_result

	def count_empty_xline(self):
		total = 0
		for x in range(self.x2, self.x1, -1):
			x_new = self.change_num_to_char(x)
			changed_address = str(x_new) + ":" + str(x_new)
			num = self.xlapp.WorksheetFunction.CountA(self.sheet_obj.Range(changed_address))
			if num == 0:
				total = total + 1
		return total

	def count_empty_xline_for_range(self, sheet_name, xyxy):
		"""
		count_emptycols(sheet_name="", xyxy)
		선택한영역에서 x줄의 값이 없으면 y줄을 삭제한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.count_empty_xline_for_range(sheet_name="", xyxy="")
			<object_name>.count_empty_xline_for_range("sht1", [1,1,3,20])
			<object_name>.count_empty_xline_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		total = 0
		for x in range(x2, x1, -1):
			x_new = self.change_num_char(x)
			changed_address = str(x_new) + ":" + str(x_new)
			num = self.xlapp.WorksheetFunction.CountA(sheet_obj.Range(changed_address))
			if num == 0:
				total = total + 1
		return total

	def count_empty_yline(self):
		total = 0
		for y in range(self.y2, self.y1, -1):
			changed_address = str(y) + ":" + str(y)
			num = self.xlapp.WorksheetFunction.CountA(self.sheet_obj.Range(changed_address))
			if num == 0:
				total = total + 1
			return total

	def count_empty_yline_for_range(self, sheet_name, xyxy):
		"""
		count_emptyrows(sheet_name="", xyxy)
		선택한영역에서 x줄의 값이 없으면 x줄을 삭제한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.count_empty_yline_for_range(sheet_name="", xyxy="")
			<object_name>.count_empty_yline_for_range("sht1", [1,1,3,20])
			<object_name>.count_empty_yline_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		total = 0
		for y in range(y2, y1, -1):
			changed_address = str(y) + ":" + str(y)
			num = self.xlapp.WorksheetFunction.CountA(sheet_obj.Range(changed_address))
			if num == 0:
				total = total + 1
			return total

	def count_max_len_for_l2d(self, input_l2d):
		input_l2d = self.check_input_data(input_l2d)
		return max(len(row) for row in input_l2d)

	def count_same_value(self):
		all_data = self.read()
		py_dic = {}
		# 읽어온 값을 하나씩 대입한다
		for line_data in all_data:
			for one_data in line_data:
				# 키가와 값을 확인
				if one_data in py_dic:
					py_dic[one_data] = py_dic[one_data] + 1
				else:
					py_dic[one_data] = 1
		self.insert_yyline(1)
		self.insert_yyline(1)
		dic_list = list(py_dic.keys())
		for no in range(len(dic_list)):
			self.sheet_obj.Cells(no + 1, 1).Value = dic_list[no]
			self.sheet_obj.Cells(no + 1, 2).Value = py_dic[dic_list[no]]

	def count_same_value_for_range(self, sheet_name, xyxy):
		"""
		 입력값 - 입력값없이 사용가능
		 선택한 영역의 반복되는 갯수를 구한다
		 - 선택한 영역에서 값을 읽어온다
		 - 사전으로 읽어온 값을 넣는다
		 - 열을 2개를 추가해서 하나는 값을 다른하나는 반복된 숫자를 넣는다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.count_same_value_for_range(sheet_name="", xyxy="")
			<object_name>.count_same_value_for_range("sht1", [1,1,3,20])
			<object_name>.count_same_value_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		all_data = self.read_value_for_range("", [x1, y1, x2, y2])
		py_dic = {}
		# 읽어온 값을 하나씩 대입한다
		for line_data in all_data:
			for one_data in line_data:
				# 키가와 값을 확인
				if one_data in py_dic:
					py_dic[one_data] = py_dic[one_data] + 1
				else:
					py_dic[one_data] = 1
		self.insert_yyline(sheet_name, 1)
		self.insert_yyline(sheet_name, 1)
		dic_list = list(py_dic.keys())
		for no in range(len(dic_list)):
			sheet_obj.Cells(no + 1, 1).Value = dic_list[no]
			sheet_obj.Cells(no + 1, 2).Value = py_dic[dic_list[no]]

	def count_sheet(self):
		"""
		현재 화성화된 엑셀 화일의 시트의 갯수

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.count_sheet()
		"""
		return self.xlbook.Worksheets.Count

	def count_workbook(self):
		"""
		열려있는 워크북의 갯수

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.count_workbook()
		"""
		result = self.xlapp.Workbooks.Count
		return result

	def count_worksheet(self):
		return self.count_sheet()

	def cut_float_by_no_of_under_point(self, no_of_under_point=3):
		"""
		선택영역안의 모든 숫자중에서, 입력받은 소숫점아래 몇번째부터, 값을 아예 삭제하는것

		:param no_of_under_point:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.cut_float_by_no_of_under_point(no_of_under_point=)
			<object_name>.cut_float_by_no_of_under_point(3)
			<object_name>.cut_float_by_no_of_under_point(2)
		"""
		sheet_obj = self.check_sheet_name("")
		x1, y1, x2, y2 = self.change_any_address_to_xyxy("")
		times = 10 ** no_of_under_point

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Value
				try:
					sheet_obj.Cells(x, y).Value = math.floor(float(one_value) * times) / times
				except:
					pass

	def cut_for_range(self, sheet_name, xyxy):
		"""
		영역을 잘라내기 하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.cut_range(sheet_name="", xyxy="")
			<object_name>.cut_range("sht1", [1,1,3,20])
			<object_name>.cut_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Cut()

	def delete(self):
		"""
		현재 선택된 영역의 모든 내용과 서식을 삭제합니다.

		:return: None

		Examples
		--------
		.. code-block:: python
		    excel.select_range("", "A1:B10")
		    excel.delete()
		"""
		self.range_obj.Clear()

	def delete_all_space_for_range(self, sheet_name, xyxy):
		"""
		입력영역안의 모든 공백을 삭제하는 것
		양쪽끝의 공백만이 아닌 문자사이의 공백도 없애는 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_all_space_for_range(sheet_name="", xyxy="")
			<object_name>.delete_all_space_for_range("sht1", [1,1,3,20])
			<object_name>.delete_all_space_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_obj.Cells(x, y).Value
				if isinstance(value, str):
					value = value.replace("", "")
					sheet_obj.Cells(x, y).Value = value

	def delete_all_value_for_sheet(self, sheet_name):
		"""
		시트안의 모든 값만을 삭제 시트를 그대로 둬야하는 경우에 사용 메뉴에서 제외

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_all_value_for_sheet(sheet_name="")
			<object_name>.delete_all_value_for_sheet("sht1")
			<object_name>.delete_all_value_for_sheet("")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.Cells.ClearContents()

	def delete_color(self):
		"""
		현재 선택된 영역의 배경색을 제거합니다.

		:return: None

		Examples
		--------
		.. code-block:: python
		    excel.select_range("", "A1:B10")
		    excel.delete_color()
		"""
		self.range_obj.Interior.Pattern = -4142
		self.range_obj.Interior.TintAndShade = 0
		self.range_obj.Interior.PatternTintAndShade = 0

	def delete_color_for_range(self, sheet_name, xyxy):
		"""
		선택한 영역안의 색을 지우는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_color_for_range(sheet_name="", xyxy="")
			<object_name>.delete_color_for_range("sht1", [1,1,3,20])
			<object_name>.delete_color_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Interior.Pattern = -4142
		range_obj.Interior.TintAndShade = 0
		range_obj.Interior.PatternTintAndShade = 0

	def delete_conditional_format(self):
		"""
		현재 선택된 영역의 모든 조건부 서식을 삭제합니다.

		:return: None

		Examples
		--------
		.. code-block:: python
		    excel.select_range("", "A1:D10")
		    excel.delete_conditional_format()
		"""
		self.range_obj.FormatConditions.Delete()

	def delete_conditional_format_for_range(self, sheet_name, xyxy):
		"""
		영역안의 모든 조건부서식을 삭제하는 기능

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_conditional_format_for_range(sheet_name="", xyxy="")
			<object_name>.delete_conditional_format_for_range("sht1", [1,1,3,20])
			<object_name>.delete_conditional_format_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.FormatConditions.Delete()

	def delete_conditional_formats_for_sheet(self, sheet_name):
		self.delete_conditional_format_all_for_sheet(sheet_name)

	def delete_continuous_same_value(self):
		tuple_2d = self.read()
		l2d = self.util.change_tuple_2d_to_l2d(tuple_2d)

		for y in range(len(l2d[0])):
			old_value = ""
			for x in range(len(l2d)):
				current_value = l2d[x][y]
				if old_value == current_value:
					l2d[x][y] = ""
				else:
					old_value = l2d[x][y]
		self.sheet_obj.Range(self.sheet_obj.Cells(self.x1, self.y1), self.sheet_obj.Cells(self.x2, self.y2)).Value = l2d

	def delete_continuous_same_value_for_range(self, sheet_name, xyxy):
		"""
		영역안의 연속된 같은 값을 지우는 것
		밑으로 같은 값들이 있으면 지우는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_continuous_same_value_for_range(sheet_name="", xyxy="")
			<object_name>.delete_continuous_same_value_for_range("sht1", [1,1,3,20])
			<object_name>.delete_continuous_same_value_for_range("", "")
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		tuple_2d = self.read_value_for_range(sheet_name, xyxy)
		l2d = self.util.change_tuple_2d_to_l2d(tuple_2d)

		for y in range(len(l2d[0])):
			old_value = ""
			for x in range(len(l2d)):
				current_value = l2d[x][y]
				if old_value == current_value:
					l2d[x][y] = ""
				else:
					old_value = l2d[x][y]
		sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2)).Value = l2d

	def delete_empty_sheets(self):
		"""
		워크북에서 빈 시트를 전부 삭제하는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_empty_sheets()
		"""
		sheets_name = self.get_sheets_name()
		for one_sheet_name in sheets_name:
			check_sheet = self.is_empty_sheet(one_sheet_name)
			if check_sheet:
				self.delete_sheet_by_name(one_sheet_name)

	def delete_empty_xline(self):
		for x in range(self.x2, self.x1 - 1, -1):
			changed_address = str(x) + ":" + str(x)
			num = self.xlapp.WorksheetFunction.CountA(self.sheet_obj.Range(changed_address))
			if num == 0:
				self.sheet_obj.Rows(changed_address).Delete()

	def delete_empty_xline_for_range(self, sheet_name, xyxy):
		"""
		현재 선택된 영역의 각x영역이 비어있으면, 전체 x라인을 삭제하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_empty_xline_for_range(sheet_name="", xyxy="")
			<object_name>.delete_empty_xline_for_range("sht1", [1,1,3,20])
			<object_name>.delete_empty_xline_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x in range(x2, x1, -1):
			xrange = sheet_obj.Range(sheet_obj.Cells(x, y1), sheet_obj.Cells(x, y2))
			num = self.xlapp.WorksheetFunction.CountA(xrange)
			if num != 0:
				changed_address = str(x) + ":" + str(x)
				sheet_obj.Rows(changed_address).Delete()

	def delete_empty_yline(self):
		for y in range(self.y2, self.y1 - 1, -1):
			cha_y = self.change_num_to_char(y)
			yrange = self.sheet_obj.Columns(cha_y)
			num = self.xlapp.WorksheetFunction.CountA(yrange)
			if num == 0:
				self.sheet_obj.Columns(cha_y).Delete()

	def delete_empty_yline_for_range(self, sheet_name, xyxy):
		"""
		현재 선택된 영역의 각x영역이 비어있으면, 전체 x라인을 삭제하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_empty_yline_for_range(sheet_name="", xyxy="")
			<object_name>.delete_empty_yline_for_range("sht1", [1,1,3,20])
			<object_name>.delete_empty_yline_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for y in range(y2, y1, -1):
			cha_y = self.change_num_to_char(y)

			yrange = sheet_obj.Range(sheet_obj.Cells(x1, y), sheet_obj.Cells(x2, y))
			num = self.xlapp.WorksheetFunction.CountA(yrange)
			if num == 0:
				changed_address = str(cha_y) + ":" + str(cha_y)
				sheet_obj.Columns(changed_address).Delete()

	def delete_file(self, old_path):
		"""
		입력으로 드러오는 화일을 삭제

		:param old_path:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_file(sheet_name="", xyxy="")
			<object_name>.delete_file("sht1", [1,1,3,20])
			<object_name>.delete_file("", "")
		"""
		old_path = self.util.check_file_path(old_path)
		os.remove(old_path)

	def delete_border_line(self):
		for each in [5, 6, 7, 8, 9, 10, 11, 12]:
			self.range_obj.Borders(each).LineStyle = -4142

	def delete_border_line_color(self):
		"""
		현재 선택된 영역의 테두리 선 색상을 제거합니다.

		:return: None

		Examples
		--------
		.. code-block:: python
		    excel.select_range("", "A1:B10")
		    excel.delete_border_line_color()
		"""
		self.range_obj.Interior.Pattern = 0
		self.range_obj.Interior.PatternTintAndShade = 0

	def delete_border_line_color_for_range(self, sheet_name, xyxy):
		"""
		영역안의 라인의 색을 지우는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_border_line_color_for_range(sheet_name="", xyxy="")
			<object_name>.delete_border_line_color_for_range("sht1", [1,1,3,20])
			<object_name>.delete_border_line_color_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Interior.Pattern = 0
		range_obj.Interior.PatternTintAndShade = 0

	def delete_border_line_for_range(self, sheet_name, xyxy):
		"""
		영역의 모든선을 지운다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_border_lines_for_range(sheet_name="", xyxy="")
			<object_name>.delete_border_lines_for_range("sht1", [1,1,3,20])
			<object_name>.delete_border_lines_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		for each in [5, 6, 7, 8, 9, 10, 11, 12]:
			range_obj.Borders(each).LineStyle = -4142

	def delete_link(self):
		"""
		현재 선택된 영역의 모든 하이퍼링크를 삭제합니다.

		:return: None

		Examples
		--------
		.. code-block:: python
		    excel.select_range("", "A1:B10")
		    excel.delete_link()
		"""
		self.range_obj.Hyperlinks.Delete()

	def delete_link_for_range(self, sheet_name, xyxy):
		"""
		선택된 영역안의 링크를 삭제하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_link_for_range(sheet_name="", xyxy="")
			<object_name>.delete_link_for_range("sht1", [1,1,3,20])
			<object_name>.delete_link_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Hyperlinks.Delete()

	def delete_memo(self):
		"""
		현재 선택된 영역의 모든 메모(주석)를 삭제합니다.

		:return: None

		Examples
		--------
		.. code-block:: python
		    excel.select_range("", "A1:B10")
		    excel.delete_memo()
		"""
		self.range_obj.ClearComments()

	def delete_memo_for_range(self, sheet_name, xyxy):
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.ClearComments()

	def delete_memos_for_sheet(self, sheet_name):
		self.delete_memos_for_sheet(sheet_name)

	def delete_nea_conditional_format_for_sheet(self, sheet_name, start_no, end_no):
		"""
		시트안의 n개의 조건부서식을 삭제하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_start: (int) 정수
		:param input_end: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_nea_conditional_format_for_sheet(sheet_name="", input_start=3, input_end=9)
			<object_name>.delete_nea_conditional_format_for_sheet("", 3, 9)
			<object_name>.delete_nea_conditional_format_for_sheet("sht1", input_start=3, input_end=9)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		for no in range(start_no, end_no + 1):
			sheet_obj.UsedRange.FormatConditions.Item(no).Delete()

	def delete_nth_char_from_left(self, start_no, end_no):
		l2d = self.read()
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = l2d[x - self.x1][y - self.y1]
			if isinstance(one_value, str):
				changed_value = one_value[:start_no - 1] + one_value[end_no:]
				self.sheet_obj.Cells(x, y).Value = changed_value

	def delete_nth_char_from_right(self, start_no, end_no):
		l2d = self.read()
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = l2d[x - self.x1][y - self.y1]
			if isinstance(one_value, str):
				if -start_no + 1 < 0:
					changed_value = one_value[:- end_no] + one_value[-start_no + 1:]
				else:
					changed_value = one_value[:- end_no]
				self.sheet_obj.Cells(x, y).Value = changed_value

	def delete_numbers(self):
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = self.sheet_obj.Cells(x, y).Value
			self.sheet_obj.Cells(x, y).Value = self.rex.delete_number_n_comma(one_value)

	def delete_numbers_for_range(self, sheet_name, xyxy):
		"""
		셀의 숫자와 ,를 삭제하는 기능

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_numbers_for_range(sheet_name="", xyxy="")
			<object_name>.delete_numbers_for_range("sht1", [1,1,3,20])
			<object_name>.delete_numbers_for_range("", "")
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Value
				sheet_obj.Cells(x, y).Value = self.rex.delete_number_n_comma(one_value)

	def delete_numbers_for_string_for_range(self, sheet_name, xyxy):
		"""
		영역안의 각셀의 값중에서 숫자를 모두 삭제하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_numbers_for_string(sheet_name="", xyxy="")
			<object_name>.delete_numbers_for_string("sht1", [1,1,3,20])
			<object_name>.delete_numbers_for_string("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Value
				if isinstance(one_value, str):
					changed_value = self.rex.delete_number_n_comma(one_value)
					sheet_obj.Cells(x, y).Value = changed_value

	def delete_paint_for_range(self, sheet_name, xyxy):
		"""
		선택한 영역안의 색을 지우는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_color(sheet_name="", xyxy="")
			<object_name>.delete_color("sht1", [1,1,3,20])
			<object_name>.delete_color("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		range_obj.Interior.Pattern = -4142
		range_obj.Interior.TintAndShade = 0
		range_obj.Interior.PatternTintAndShade = 0

	def delete_panthom_link(self):
		"""
		이름영역중에서 연결이 끊긴것을 삭제하는 것
		"""
		names_count = self.xlbook.Names.Count
		del_count = 0
		if names_count > 0:
			for aaa in range(names_count, 0, -1):
				name_name = self.xlbook.Names(aaa).Name
				name_range = self.xlbook.Names(aaa)

				if "#ref!" in str(name_range).lower():
					print("found panthom link!!! ===> ", name_name)
					self.xlapp.Names(aaa).Delete()
					del_count = del_count + 1
		print("Deleted Nos ==> ", del_count)

	def delete_partial_value_as_eng_char(self):
		result = []
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = self.sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				changed_one_value = re.sub(r'[a-zA-Z]', '', one_value)
				if one_value != changed_one_value:
					self.sheet_obj.Cells(x, y).Value = changed_one_value

	def delete_partial_value_between_a_and_b(self, input_list):
		input_list = self.check_input_data(input_list)
		input_list[0] = str(input_list[0]).strip()
		input_list[1] = str(input_list[1]).strip()

		special_char = ".^$*+?{}[]\\|()"
		# 특수문자는 역슬래시를 붙이도록
		if input_list[0] in special_char: input_list[0] = "\\" + input_list[0]
		if input_list[1] in special_char: input_list[1] = "\\" + input_list[1]
		re_basic = str(input_list[0]) + ".*" + str(input_list[1])

		# 찾은값을 넣을 y열을 추가한다
		new_x = int(self.x2) + 1
		self.insert_yyline(new_x)
		for y in range(self.y1, self.y2 + 1):
			temp = ""
			for x in range(self.x1, self.x2 + 1):
				one_value = self.sheet_obj.Cells(x, y).Value2
				result_list = re.findall(re_basic, str(one_value))

				if result_list == None or result_list == []:
					pass
				else:
					temp = temp + str(result_list)
					self.sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint("yel++")
			self.sheet_obj.Cells(y, new_x).Value = temp

	def delete_partial_value_for_range_as_eng_char(self, sheet_name, xyxy):
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		result = []
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Value
				if isinstance(one_value, str):
					changed_one_value = re.sub(r'[a-zA-Z]', '', one_value)
					if one_value != changed_one_value:
						sheet_obj.Cells(x, y).Value = changed_one_value

	def delete_partial_value_for_range_as_int_char(self, sheet_name, xyxy):
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		result = []
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Value
				if isinstance(one_value, str):
					changed_one_value = re.sub(r'[0-9]', '', one_value)
					if one_value != changed_one_value:
						sheet_obj.Cells(x, y).Value = changed_one_value

	def delete_partial_value_for_range_as_int_n_eng_char(self):
		result = []
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = self.sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				changed_one_value = re.sub(r'[a-zA-Z0-9]', '', one_value)
				if one_value != changed_one_value:
					self.sheet_obj.Cells(x, y).Value = changed_one_value

	def delete_partial_value_for_range_between_specific_letter(self, sheet_name, xyxy, input_list=["(", ")"],
											 mark_color="yel++", keep_log=False):
		"""
		선택된 영역의 셀에서 특정 문자 사이의 값을 삭제 (특수문자 포함)

		예: "abc(def)gh" => "abcgh"
			"test[123]end" => "testend"
			"a(b)c(d)e" => "ace" (여러 개 모두 삭제)

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_list: 시작/끝 문자 리스트 [시작, 끝] 예: ["(", ")"], ["[", "]"]
		:param mark_color: 변경된 셀의 색상 (기본: "yel++")
		:param keep_log: 삭제된 내용을 옆 열에 기록할지 여부
		:return: (dict) 처리 결과 통계

		Examples
		--------
		.. code-block:: python
			   # 괄호 안 내용 삭제
			   <object_name>.delete_value_between_specific_letter("sht1", "A1:C10", ["(", ")"])

			   # 대괄호 안 내용 삭제, 로그 남기기
			   <object_name>.delete_value_between_specific_letter("sht1", "", ["[", "]"], keep_log=True)

			   # 중괄호 안 내용 삭제, 색상 없이
			   <object_name>.delete_value_between_specific_letter("sht1", "", ["{", "}"], mark_color=None)
		"""
		import re

		try:
			# 입력 처리
			input_list = self.check_input_data(input_list)
			if len(input_list) != 2:
				raise ValueError("input_list는 [시작문자, 끝문자] 형태여야 합니다")

			sheet_obj = self.check_sheet_name(sheet_name)
			[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

			# 특수문자 이스케이프 처리
			start_char = str(input_list[0]).strip()
			end_char = str(input_list[1]).strip()

			# re.escape를 사용하여 특수문자 자동 처리
			escaped_start = re.escape(start_char)
			escaped_end = re.escape(end_char)

			# 정규식 패턴: non-greedy 매칭 사용 (.*? 대신 .*?)
			# 중첩 괄호를 고려하지 않는 단순 버전
			pattern = f"{escaped_start}.*?{escaped_end}"

			# 통계
			stats = {
				'total_cells': 0,
				'modified_cells': 0,
				'deleted_patterns': 0
			}

			# 로그 열 추가 (옵션)
			log_col = None
			if keep_log:
				log_col = y2 + 1
				self.insert_yline(sheet_name, log_col)

			# 셀 순회 및 처리
			for x in range(x1, x2 + 1):  # 행 (row)
				for y in range(y1, y2 + 1):  # 열 (column)
					stats['total_cells'] += 1

					# 원본 값 읽기
					original_value = sheet_obj.Cells(x, y).Value

					# None이나 빈 값 건너뛰기
					if original_value is None or original_value == "":
						continue

					original_str = str(original_value)

					# 패턴 찾기
					matches = re.findall(pattern, original_str)

					if matches:
						# 패턴 삭제
						modified_str = re.sub(pattern, "", original_str)

						# 실제로 변경된 경우만 처리
						if modified_str != original_str:
							# 값 업데이트
							sheet_obj.Cells(x, y).Value = modified_str

							# 색상 표시
							if mark_color:
								try:
									color_rgb = self.color.change_any_color_to_rgbint(mark_color)
									sheet_obj.Cells(x, y).Interior.Color = color_rgb
								except:
									pass  # 색상 적용 실패해도 계속 진행

							# 로그 기록
							if keep_log and log_col:
								deleted_info = " | ".join(matches)
								sheet_obj.Cells(x, log_col).Value = deleted_info

							# 통계 업데이트
							stats['modified_cells'] += 1
							stats['deleted_patterns'] += len(matches)

			# 결과 출력
			print(f"\n{'=' * 50}")
			print(f"삭제 패턴: {start_char}...{end_char}")
			print(f"처리 영역: {sheet_obj.Name} [{x1},{y1}] ~ [{x2},{y2}]")
			print(f"총 셀 수: {stats['total_cells']}")
			print(f"수정된 셀: {stats['modified_cells']}")
			print(f"삭제된 패턴 수: {stats['deleted_patterns']}")
			print(f"{'=' * 50}\n")

			return stats

		except Exception as e:
			print(f"✗ delete_value_between_specific_letter 오류: {str(e)}")
			raise

	def delete_partial_value_for_range_by_from0toN(self, sheet_name, xyxy, input_no):
		"""
		영역안의 모든 셀값을중, 앞에서부터 입력으로 들어온 N까지의 글자를 삭제하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_no: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_each_cell_value_from0toN_for_range(sheet_name="", xyxy="", input_no=7)
			<object_name>.delete_each_cell_value_from0toN_for_range("", "", 7)
			<object_name>.delete_each_cell_value_from0toN_for_range(sheet_name="sht1", xyxy = [1,1,3,7], input_no=7)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):

				one_value = sheet_obj.Cells(x, y).Value2
				if one_value != "" or one_value != None :
					sheet_obj.Cells(x, y).Value = one_value[int(input_no):]

	def delete_partial_value_for_range_by_left_nth_char(self, sheet_name, xyxy, input_no):
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Value
				if isinstance(one_value, str):
					sheet_obj.Cells(x, y).Value = one_value[input_no:]

	def delete_partial_value_for_range_from0toN_at_end(self, sheet_name, xyxy, input_no):
		"""
		영역안의 모든 셀값을중, 앞에서부터 입력으로 들어온 N까지의 글자를 삭제하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_no: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_from0toN_at_end(sheet_name="", xyxy="", input_no=7)
			<object_name>.delete_from0toN_at_end("", "", 7)
			<object_name>.delete_from0toN_at_end(sheet_name="sht1", xyxy = [1,1,3,7], input_no=7)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Value2
				if one_value != "" or one_value != None :
					sheet_obj.Cells(x, y).Value = one_value[:- int(input_no)]

	def delete_partial_value_for_range_from0toN_at_start(self, sheet_name, xyxy, input_no):
		"""
		영역안의 모든 셀값을중, 앞에서부터 입력으로 들어온 N까지의 글자를 삭제하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_no: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_from0toN_at_start_for_range(sheet_name="", xyxy="", input_no=7)
			<object_name>.delete_from0toN_at_start_for_range("", "", 7)
			<object_name>.delete_from0toN_at_start_for_range(sheet_name="sht1", xyxy = [1,1,3,7], input_no=7)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Value2
				if isinstance(one_value, str):
					sheet_obj.Cells(x, y).Value = one_value[int(input_no):]

	def delete_partial_value_for_range_right_nth_char_for_range(self, sheet_name, xyxy, input_no):
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Value
				if isinstance(one_value, str):
					sheet_obj.Cells(x, y).Value = one_value[:-input_no]

	def delete_partial_value_for_range_right_value_from_1st_found_position_by_rex(self, input_xre):
		"""
		처음 찾은 자료의 오른쪽의 모든 자료를 삭제하는것

		:param input_xre: (str) xre형식의 문자열, 예는 "[시작:처음][영어:1~4][한글:3~10]"
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_right_value_from_1st_found_position_by_rex(input_xre="[영어:1~4][한글:3~10]")
			<object_name>.delete_right_value_from_1st_found_position_by_rex("[영어:1~4][한글:3~10]")
			<object_name>.delete_right_value_from_1st_found_position_by_rex(input_xre="[시작:처음][영어:1~4][한글:3~10]")
		"""
		sheet_obj = self.check_sheet_name("")
		xyxy = self.get_address_for_selection()
		for x in range(xyxy[0], xyxy[2] + 1):
			for y in range(xyxy[1], xyxy[3] + 1):
				one_value = sheet_obj.Cells(x, y).Value
				aaa = self.rex.search_all_by_xsql(input_xre, one_value)
				if aaa:
					temp = one_value[:int(aaa[0][2])]
				sheet_obj.Cells(x, y).Value = temp

	def delete_range_names(self):
		"""
		모든 range_name을 삭제하는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_range_names()
		"""
		for one_range_name in self.xlapp.Names:
			ddd = str(one_range_name.Name)
			if ddd.find("!") < 0:
				self.xlbook.Names(ddd).Delete()

	def delete_same_value(self):
		"""
		같은것중에 하나는 남겨놓아야 한다
		그렇지 않으면, 전부 삭제하는것과 같기 때문이다
		:return:
		"""
		self.delete_same_value_over_n_times(2)

	def delete_same_value_over_n_times(self, input_no=2):
		"""
		n번째 반복되는 것들만 삭제한다
		1로 하면, 전체가 다 삭제되는것과 같다
		:return:
		"""
		unique_dic = {}
		l2d = self.read()
		for ix, l1d in enumerate(l2d):
			for iy, one_value in enumerate(l1d):
				if one_value:
					if one_value in unique_dic.keys():
						unique_dic[one_value] = unique_dic[one_value] +1
					else:
						unique_dic[one_value] = 1

					if 	unique_dic[one_value] >= input_no:
						self.sheet_obj.Cells(self.x1 + ix, self.y1 + iy).Value = ""

	def delete_same_value_for_range_over_n_times(self, sheet_name, xyxy, input_no):
		"""
		n번째 반복되는 것들만 삭제한다
		1로 하면, 전체가 다 삭제되는것과 같다
		:return:
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		l2d = range_obj.Value

		unique_dic = {}
		for ix, l1d in enumerate(l2d):
			for iy, one_value in enumerate(l1d):
				if one_value:
					if one_value in unique_dic.keys():
						unique_dic[one_value] = unique_dic[one_value] +1
					else:
						unique_dic[one_value] = 1

					if 	unique_dic[one_value] >= input_no:
						sheet_obj.Cells(self.x1 + ix, self.y1 + iy).Value = ""

	def delete_same_value_except_first_one(self):
		self.delete_same_value_over_n_times(2)

	def delete_same_value_for_range(self, sheet_name, xyxy):
		"""
		선택된 영역안의 같은 값을 지우는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_same_value_for_range(sheet_name="", xyxy="")
			<object_name>.delete_same_value_for_range("sht1", [1,1,3,20])
			<object_name>.delete_same_value_for_range("", "")
		"""
		self.delete_same_value_for_range_over_n_times(sheet_name, xyxy, 2)

	def delete_same_xline(self):
		all_values = self.read()
		for no in range(len(all_values)):
			self.sheet_obj.Range(self.sheet_obj.Cells(no + self.x1, self.y1),
								 self.sheet_obj.Cells(no + self.x1, self.y2)).ClearContents()

	def delete_same_xline_for_range(self, sheet_name, xyxy, input_list):
		"""
		입력영역의 같은 자료 삭제

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_same_xline_for_range(sheet_name="", xyxy="", input_list=[1, "abc", "가나다"])
			<object_name>.delete_same_xline_for_range("", "", [1, "abc", "가나다"])
			<object_name>.delete_same_xline_for_range("sht1", "", [1, "abc", "가나다"])
		"""
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		for x in range(x2, x1 - 1, -1):
			temp = self.read_value_for_range(sheet_name, [x, y1, x, y1 + len(input_list[0] - 1)])
			if input_list == temp:
				self.delete_xline(sheet_name, [x, x])

	def delete_shape_by_name(self, sheet_name, shape_name):
		"""
		객체의 이름으로 제거하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param shape_name: (str) 입력으로 들어오는 텍스트, 도형/그림객체의 이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_shape_by_name(sheet_name="", shape_name="name1")
			<object_name>.delete_shape_by_name("", "name1")
			<object_name>.delete_shape_by_name(sheet_name="sht1", shape_name="name1")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.Shapes(shape_name).Delete()

	def delete_shape_by_no_for_sheet(self, sheet_name, input_no):
		"""
		시트안의 모든 객체를 삭제하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_shape_by_no_for_sheet(sheet_name="", input_no=7)
			<object_name>.delete_shape_by_no_for_sheet("", 7)
			<object_name>.delete_shape_by_no_for_sheet(sheet_name="sht1", input_no=7)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.Shapes(input_no).Delete()

	def delete_shapes(self):
		"""
		현재 활성 시트의 모든 도형/그림 객체를 삭제합니다.

		:return: 삭제된 객체 수

		Examples
		--------
		.. code-block:: python
		    count = excel.delete_shapes()
		    print(f"{count}개의 객체가 삭제되었습니다.")
		"""
		drawings_nos = self.sheet_obj.Shapes.Count
		if drawings_nos > 0:
			for num in range(drawings_nos, 0, -1):
				# Range를 앞에서부터하니 삭제하자마자 번호가 다시 매겨져서, 뒤에서부터 삭제하니 잘된다
				self.sheet_obj.Shapes(num).Delete()
		return drawings_nos

	def delete_shapes_for_sheet(self, sheet_name):
		"""
		시트안의 모든 객체를 삭제하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_shapes_for_sheet(sheet_name="")
			<object_name>.delete_shapes_for_sheet("sht1")
			<object_name>.delete_shapes_for_sheet("")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		drawings_nos = sheet_obj.Shapes.Count

		if drawings_nos > 0:
			for num in range(drawings_nos, 0, -1):
				# Range를 앞에서부터하니 삭제하자마자 번호가 다시 매겨져서, 뒤에서부터 삭제하니 잘된다
				sheet_obj.Shapes(num).Delete()
		return drawings_nos

	def delete_sheet_by_name(self, sheet_name):
		"""
		시트하나 삭제하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_sheet_by_name(sheet_name="")
			<object_name>.delete_sheet_by_name("sht1")
			<object_name>.delete_sheet_by_name("")
		"""
		try:
			sheet_obj = self.check_sheet_name(sheet_name)
			self.xlapp.DisplayAlerts = False
			sheet_obj.Delete()
			self.xlapp.DisplayAlerts = True
		except:
			pass

	def delete_sheet_by_no(self, input_no):
		"""
		앞에서부터 n번째의 시트를 삭제하는 것

		:param input_no: (int) 정수, 입력으로 들어오는 숫자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_sheet_by_no(input_no=3)
			<object_name>.delete_sheet_by_no(5)
			<object_name>.delete_sheet_by_no(7)
		"""
		sheets_name_list = self.get_sheet_names()
		self.delete_sheet_by_name(sheets_name_list[input_no - 1])

	def delete_tab_color_by_sheet_name(self, sheet_name):
		"""
		시트탭의 색을 넣는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_tab_color_by_sheet_name(sheet_name="")
			<object_name>.delete_tab_color_by_sheet_name("sht1")
			<object_name>.delete_tab_color_by_sheet_name("")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.Tab.ColorIndex = -4142
		sheet_obj.Tab.TintAndShade = 0

	def delete_text_num(self):
		result = []
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = self.sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				changed_one_value = re.sub(r'[0-9]', '', one_value)
				if one_value != changed_one_value:
					self.sheet_obj.Cells(x, y).Value = changed_one_value

	def delete_text_num_n_comma(self):
		for x in range(self.x1, self.x2 + 1):
			for y in range(self.y1, self.y2 + 1):
				value = self.read_value_for_cell("", [x, y])
				if isinstance(value, str):
					changed_value = self.rex.delete_number_n_comma(value)
					self.sheet_obj.Cells(x, y).Value = changed_value

	def delete_textboxes(self, sheet_name):
		"""
		모든 텍스트박스 지우기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_textboxes(sheet_name="")
			<object_name>.delete_textboxes("sht1")
			<object_name>.delete_textboxes("")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		for shape in sheet_obj.Shapes:
			if shape.Tyde == 17:
				shape.Delete()

	def delete_value(self):
		"""
		현재 선택된 영역의 값만 삭제합니다 (서식은 유지).

		:return: None

		Examples
		--------
		.. code-block:: python
		    excel.select_range("", "A1:B10")
		    excel.delete_value()
		"""
		self.range_obj.ClearContents()

	def delete_value_by_step(self, step_no):
		"""
		영역안의 자료의 n번째마다 반복되는 값을 삭제
		:param step_no:
		:return:
		"""
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			if divmod(x+y-1, step_no)[1] == 0:
				self.sheet_obj.Cells(x, y).ClearContents()

	def delete_value_for_cell(self, sheet_name, xyxy):
		"""
		선택한 셀의 값을 삭제하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_value_for_cell(sheet_name="", xyxy="")
			<object_name>.delete_value_for_cell("sht1", [1,1,3,20])
			<object_name>.delete_value_for_cell("", "")
		"""
		self.delete_value_for_range(sheet_name, xyxy)

	def delete_value_for_range(self, sheet_name, xyxy):
		"""
		delete_value(sheet_name="", xyxy)
		range의 입력방법은 [row1, col1, row2, col2]이다
		선택한 영역안의 모든 값을 지운다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_value_for_range(sheet_name="", xyxy="")
			<object_name>.delete_value_for_range("sht1", [1,1,3,20])
			<object_name>.delete_value_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.ClearContents()

	def delete_value_for_range_between_specific_letter(self, sheet_name, xyxy, input_list=["(", ")"]):
		"""
		선택된 영역안의 값중에서 입력된 특수문자 사이의 값을 삭제하는 것
		입력자료의 두사이의 자료를 포함하여 삭제하는것
		예: abc(def)gh ==>abcgh

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_value_for_range_between_specific_letter(sheet_name="", xyxy="", input_list=["(", ")"])
			<object_name>.delete_value_for_range_between_specific_letter("", "", ["(", ")"])
			<object_name>.delete_value_for_range_between_specific_letter("sht1", "", input_list=["(", ")"])
		"""
		input_list = self.check_input_data(input_list)

		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		input_list[0] = str(input_list[0]).strip()
		input_list[1] = str(input_list[1]).strip()

		special_char = ".^$*+?{}[]\\|()"
		# 특수문자는 역슬래시를 붙이도록
		if input_list[0] in special_char: input_list[0] = "\\" + input_list[0]
		if input_list[1] in special_char: input_list[1] = "\\" + input_list[1]
		re_basic = str(input_list[0]) + ".*" + str(input_list[1])

		# 찾은값을 넣을 y열을 추가한다
		new_x = int(x2) + 1
		self.insert_yline(sheet_name, new_x)
		for y in range(y1, y2 + 1):
			temp = ""
			for x in range(x1, x2 + 1):
				one_value = sheet_obj.Cells(x, y).Value2
				result_list = re.findall(re_basic, str(one_value))

				if result_list == None or result_list == []:
					pass
				else:
					temp = temp + str(result_list)
					sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint("yel++")
			sheet_obj.Cells(y, new_x).Value = temp

	def delete_value_for_range_by_step(self, sheet_name, xyxy, step_no=1):
		"""
    선택한 영역 내에서 n번째 행마다 값만 삭제합니다 (행 자체는 유지).

    :param sheet_name: 시트이름, ""은 현재 활성화된 시트이름을 뜻함
    :param xyxy: 영역의 형태로 ""(현재 선택영역), A1:B3, [1,1,2,2]은 [왼쪽위의 row,왼쪽 위의 col, 오른쪽 아래의 row,오른쪽 아래의 col]
    :param step_no: 반복 간격 (예: 3이면 3, 6, 9번째 행 삭제)
    :return: None

    Examples
    --------
    .. code-block:: python
        # 3번째마다 행 값 삭제
        excel.delete_value_for_range_by_step("Sheet1", "A1:D100", 3)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			if divmod(x - x1 + 1, step_no)[1] == 0:
				sheet_obj.Range(sheet_obj.Cells(x, y1), sheet_obj.Cells(x, y2)).ClearContents()

	def delete_value_for_range_for_same_value_by_many_same_column(self, sheet_name, xyxy):
		"""
		영역안의 같은 값을 지우는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_value_for_range_for_same_value_by_many_same_column(sheet_name="", xyxy="")
			<object_name>.delete_value_for_range_for_same_value_by_many_same_column("sht1", [1,1,3,20])
			<object_name>.delete_value_for_range_for_same_value_by_many_same_column("", [1,9,6,87])
		"""
		self.delete_xxline_value_for_range_by_same_line(sheet_name, xyxy)

	def delete_value_for_range_name(self, range_name="name1"):
		"""
		입력한 영역의 이름을 삭제

		:param range_name: (str) 입력으로 들어오는 텍스트, 영역이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_range_name(range_name="영역이름1")
			<object_name>.delete_range_name("영역이름1")
			<object_name>.delete_range_name("영역이름123")
		"""
		result = self.xlbook.Names(range_name).Delete()
		return result

	def delete_value_for_usedrange(self, sheet_name):
		"""
		자주사용하는 것 같아서 usedrange의 값을 지우는것을 만들어 보았다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_value_for_usedrange(sheet_name="")
			<object_name>.delete_value_for_usedrange("sht1")
			<object_name>.delete_value_for_usedrange("")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		temp_range = self.read_usedrange_address(sheet_name)
		sheet_obj.Range(temp_range[2]).ClearContents()

	def delete_vba_module_by_name_list(self, module_name_list):
		"""
		열려있는 화일안에서 입력리스트의 메크로를 삭제를 하는 것

		:param module_name_list:리스트형, 메크로 모듈이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_vba_module_by_name_list(module_name_list=["name1", "name3"])
			<object_name>.delete_vba_module_by_name_list(["name1", "name3"])
		"""
		for module_name in module_name_list:
			xlmodule = self.xlbook.VBProject.VBComponents(module_name)
			self.xlbook.VBProject.VBComponents.Remove(xlmodule)

	def delete_xline(self, *input_l1d):
		"""
    지정한 행들을 삭제합니다 (행 자체를 제거).

    :param input_l1d: 삭제할 행 번호들 (가변 인자)
    :return: None

    Examples
    --------
    .. code-block:: python
        excel.delete_xline(1, 5, 10)  # 1, 5, 10번 행 삭제
		"""
		input_l1d = self.check_input_list(input_l1d)
		for ix, no in enumerate(input_l1d):
			self.sheet_obj.Rows(str(no-ix) + ':' + str(no-ix)).Delete()

	def delete_xline_for_range(self, sheet_name, input_l1d):
		"""
		선택한영역에서 x줄의 값이 없으면 x줄을 삭제한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xx_list: (list) 가로줄의 사작과 끝 => [3,7], [2, 4], 2~4까지의 x줄
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_xline(sheet_name="", xx_list=[3,5])
			<object_name>.delete_xline("", [1,7])
			<object_name>.delete_xline(sheet_name="sht1", xx_list=[3,5])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		input_l1d = self.check_input_list(input_l1d)

		for ix, no in enumerate(input_l1d):
			sheet_obj.Rows(str(no-ix) + ':' + str(no-ix)).Delete()

	def delete_xline_for_range_by_step(self, sheet_name, xyxy, step_no=1):
		"""
		선택영역안의 => 선택한 n번째 가로행을 삭제한다. 값만 삭제하는것이 아니다
		위에서부터 삭제가 되게 만든것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param step_no: (int) 번호, 반복되는 횟수의 번호, step의 의미 : 간격을 두고 값을 쓸때 (예 : 현재 위치를 기준으로 가로로 2칸씩, 세로로 3칸씩 반복되는 위치에 쓸때)
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_xline_by_step_for_range(sheet_name="", xyxy="", step_no=7)
			<object_name>.delete_xline_by_step_for_range("", "", 7)
			<object_name>.delete_xline_by_step_for_range(sheet_name="sht1", xyxy = [1,1,3,7], step_no=7)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for ix, no in enumerate(range(x1, x2+1, step_no)):
			sheet_obj.Rows(str(no-ix) + ':' + str(no-ix)).Delete()

	def delete_xline_for_range_when_same_multi_y_lines(self, sheet_name, xyxy, input_no_list=[1, 2, 3, 4]):
		"""
		여러줄의 값이 같은것만 삭제하는것
		[1, 3, 5]값이 다 같은 것만 삭제하는것

		:param self:

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_xline_when_same_multi_y_lines(sheet_name="", xyxy="", input_no_list=[1,2,3,4])
			<object_name>.delete_xline_when_same_multi_y_lines("", "", [1,2,3,4])
			<object_name>.delete_xline_when_same_multi_y_lines("sht1", "", [1,2,3,4])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		l2d = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2)).Value

		filtered_l2d = []
		for l1d in l2d:
			new_row = []
			for idx in input_no_list:
				new_row.append(l1d[idx-1])
			filtered_l2d.append(new_row)

		temp_set = set()
		for ix, l1d in enumerate(filtered_l2d):
			if l1d in temp_set:
				sheet_obj.Range(sheet_obj.Cells(ix + x1+1, y1), sheet_obj.Cells(ix + x1+1, y2)).ClearContents()

	def delete_xline_value(self, *input_l1d):
		input_l1d = self.check_input_list(input_l1d)
		for ix, no in enumerate(input_l1d):
			self.sheet_obj.Rows(str(no) + ':' + str(no)).ClearContents()

	def delete_xline_value_for_range_by_step(self, sheet_name, xyxy, step_no=1):
		"""
		삭제 : 2 ==> 기존의 2번째 마다 삭제 (1,2,3,4,5,6,7 => 1,3,5,7)
		삭제 : 선택자료중 n번째 세로줄의 자료를 값만 삭제하는것
		일하다보면 3번째 줄만 삭제하고싶은경우가 있다, 이럴때 사용하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param step_no: (int) 번호, 반복되는 횟수의 번호, step의 의미 : 간격을 두고 값을 쓸때 (예 : 현재 위치를 기준으로 가로로 2칸씩, 세로로 3칸씩 반복되는 위치에 쓸때)
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_xline_value_by_step(sheet_name="", xyxy="", step_no=7)
			<object_name>.delete_xline_value_by_step("", "", 7)
			<object_name>.delete_xline_value_by_step(sheet_name="sht1", xyxy = [1,1,3,7], step_no=7)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for ix, no in enumerate(range(x1, x2+1, step_no)):
			sheet_obj.Rows(str(no) + ':' + str(no)).ClearContents()

	def delete_xline_value_for_range_when_same_multi_y_line_value(self, sheet_name, xyxy, input_no_list):
		"""
		2차원의 자료에서 여러 y줄의 값이 제일위의것과 같은 줄을 전체를 삭제하는것
		:param sheet_name:
		:param xyxy:
		:param input_no_list:
		:return:
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		l2d = range_obj.Value
		#unique_l2d = self.get_unique_columns_basic(l2d, input_no_list)

		top_line = [tuple(l2d[0][i] for i in input_no_list)]

		for ix, l1d in enumerate(l2d):
			changed_l1d = [tuple(l1d[i] for i in input_no_list)]
			if top_line == changed_l1d:
				sheet_obj.Rows(str(ix + x1) + ':' + str(ix + x1)).ClearContents()

	def delete_xline_value_for_range_when_same_multi_y_lines(self, sheet_name, xyxy, input_no_list):
		"""
		2차원의 자료에서 여러 y줄의 값이같을때 제일 처음의것만 남기고 나머지는 줄을 전체를 삭제하는것
		:param sheet_name:
		:param xyxy:
		:param input_no_list:
		:return:
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		l2d = range_obj.Value

		unique_set = set()

		for ix, l1d in enumerate(l2d):
			changed_l1d = [tuple(l1d[i] for i in input_no_list)]
			if changed_l1d in unique_set:
				sheet_obj.Rows(str(ix + x1) + ':' + str(ix + x1)).ClearContents()
			else:
				unique_set.add(changed_l1d)

	def delete_xline_value_when_same_multi_y_lines(self, input_no_list):
		l2d = self.read()
		unique_l2d = self.get_unique_columns_basic(l2d, input_no_list)

		for base_l1d in unique_l2d:
			found_count = 0
			for ix, l1d in enumerate(l2d):
				changed_l1d = [tuple(l1d[i] for i in input_no_list)]
				if base_l1d == changed_l1d:
					if found_count > 0:
						self.sheet_obj.Rows(str(ix + self.x1) + ':' + str(ix + self.x1)).ClearContents()
					found_count = found_count + 1

	def delete_xxline(self, *input_l1d):
		"""
		지정한 범위의 연속된 열들을 삭제합니다.

		:param yy_list: [시작열, 끝열]
		:return: None

		Examples
		--------
		.. code-block:: python
			excel.delete_yyline([2, 5])  # 2~5번 열 삭제
		"""
		input_l1d = self.check_input_list(input_l1d)
		self.sheet_obj.Rows(str(input_l1d[0]) + ':' + str(input_l1d[1])).Delete()

	def delete_xxline_for_sheet(self, sheet_name, xx_list):
		"""
		선택한영역에서 x줄의 값이 없으면 x줄을 삭제한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xx_list: (list) 가로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_xxline_for_sheet(sheet_name="", xx_list=[3,5])
			<object_name>.delete_xxline_for_sheet("", [1,7])
			<object_name>.delete_xxline_for_sheet(sheet_name="sht1", xx_list=[3,5])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		new_xx = self.check_xx_address(xx_list)
		sheet_obj.Rows(str(new_xx[0]) + ':' + str(new_xx[1])).Delete()

	def delete_xxline_value_for_range_by_same_line(self, sheet_name, xyxy):
		"""
		한줄씩 비교를 해서, 줄의 모든 값이 똑같으면 처음것을 제외하고 다음 자료부터 값만 삭제하는 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_xxline_value_for_range_by_same_line(sheet_name="", xyxy="")
			<object_name>.delete_xxline_value_for_range_by_same_line("sht1", [1,1,3,20])
			<object_name>.delete_xxline_value_for_range_by_same_line("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		l2d = self.read_value_for_range(sheet_name, xyxy)
		unique_set = set()

		for ix, l1d in enumerate(l2d):
			if l1d in unique_set:
				sheet_obj.Rows(str(ix + x1) + ':' + str(ix + x1)).ClearContents()
			else:
				unique_set.add(l1d)

	def delete_yline(self, *input_l1d):
		"""
		지정한 열들을 삭제합니다 (열 자체를 제거).

		:param input_l1d: 삭제할 열 번호들 (가변 인자)
		:return: None

		Examples
		--------
		.. code-block:: python
		    excel.delete_yline(1, 3, 5)  # 1, 3, 5번 열 삭제
		"""
		input_l1d = self.check_input_list(input_l1d)
		for iy, no in enumerate(input_l1d):
			char_no = self.change_num_to_char(no-iy)
			self.sheet_obj.Columns(str(char_no) + ':' + str(char_no)).Delete()

	def delete_yline_value(self, *input_l1d):
		input_l1d = self.check_input_list(input_l1d)
		for iy, no in enumerate(input_l1d):
			char_no = self.change_num_to_char(no)
			self.sheet_obj.Columns(str(char_no) + ':' + str(char_no)).ClearContents()


	def delete_yline_by_step(self, step_no):
		current_no = 0
		for y in range(1, self.y2 - self.y1 + 1):
			mok, namuji = divmod(y, int(step_no))
			if namuji == 0:
				self.delete_yyline([current_no + self.y1, current_no + self.y1])
			else:
				current_no = current_no + 1

	def delete_yline_for_range_by_step(self, sheet_name, xyxy, step_no):
		"""
		선택한 영역안의 세로줄중에서 선택한 몇번째마다 y라인을 삭제하는것
		(선택한 영역안에서 3번째 마다의 y라인을 삭제하는것)

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param step_no: (int) 번호, 반복되는 횟수의 번호, step의 의미 : 간격을 두고 값을 쓸때 (예 : 현재 위치를 기준으로 가로로 2칸씩, 세로로 3칸씩 반복되는 위치에 쓸때)
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_yline_by_step_for_range(sheet_name="", xyxy="", step_no=7)
			<object_name>.delete_yline_by_step_for_range("", "", 7)
			<object_name>.delete_yline_by_step_for_range(sheet_name="sht1", xyxy = [1,1,3,7], step_no=7)
		"""
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		current_no = 0
		for y in range(1, y2 - y1 + 1):
			mok, namuji = divmod(y, int(step_no))
			if namuji == 0:
				self.delete_yline(sheet_name, [current_no + y1, current_no + y1])
			else:
				current_no = current_no + 1

	def delete_yline_for_range_for_empty_yline(self, sheet_name, xyxy):
		"""
		현재 선택된 영역안에서 y라인이 모두 빈것을 삭제하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_yline_for_range_for_empty_yline(sheet_name="", xyxy="")
			<object_name>.delete_yline_for_range_for_empty_yline("sht1", [1,1,3,20])
			<object_name>.delete_yline_for_range_for_empty_yline("", "")
		"""
		self.delete_empty_yline_for_range(sheet_name, xyxy)

	def delete_yline_value_by_step_for_range(self, sheet_name, xyxy, step_no):
		"""
		선택한 영역안의 세로줄중에서 선택한 몇번째마다 y라인의 값을 삭제하는것
		(선택한 영역안에서 3번째 마다의 y라인의 값을 삭제하는것)

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param step_no: (int) 번호, 반복되는 횟수의 번호, step의 의미 : 간격을 두고 값을 쓸때 (예 : 현재 위치를 기준으로 가로로 2칸씩, 세로로 3칸씩 반복되는 위치에 쓸때)
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_yline_value_by_step_for_range(sheet_name="", xyxy="", step_no=7)
			<object_name>.delete_yline_value_by_step_for_range("", "", 7)
			<object_name>.delete_yline_value_by_step_for_range(sheet_name="sht1", xyxy = [1,1,3,7], step_no=7)
		"""
		self.self.delete_yline_by_step_for_range(sheet_name, xyxy, step_no)

	def delete_ylines_for_input_l2d(self, input_l2d, no_list):
		input_l2d = self.check_input_data(input_l2d)
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_l2d)):
				del input_l2d[x][one]
		return input_l2d

	def delete_ylines_input_l2d_for_yline_nos(self, input_l2d, no_list):
		"""
		입력으로받은 번호리스트를 기준으로 2차원의 자료를 삭제하는 것

		:param input_l2d: (list) 2차원의 list형 자료
		:param no_list:  (list) 1차원의 list형 자료
		:return:
		Examples
		--------
		.. code-block:: python
			<object_name>.delete_ylines_input_l2d_for_yline_nos(input_l2d=[[1, 2], [4, 5]], no_list=[1, 3, 5])
			<object_name>.delete_ylines_input_l2d_for_yline_nos([[1, 2], [4, 5]], [1, 3, 5])
			<object_name>.delete_ylines_input_l2d_for_yline_nos(input_l2d=[[1, 2], [4, 5]], no_list=[6,8,14])
		"""
		input_l2d = self.check_input_data(input_l2d)
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_l2d)):
				del input_l2d[x][one]
		return input_l2d

	def delete_yyline(self, yy_list):
		y1, self.y2 = self.check_yy_address(yy_list)
		self.sheet_obj.Columns(self.y1 + ':' + self.y1).Delete()

	def draw_border_line_for_range(self, sheet_name, xyxy, position="all", xcolor="bla", thickness="thin", style="-"):
		# 내부적으로 들어오는 형태가 튜플로 2차원까지 문제가 될소지가 있어 변경하는 부분이다
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		thickness = self.varx["check_line_thickness"][thickness]
		style = self.varx["line_style_vs_enum"][style]
		position = self.varx["check_line_position"][position]
		color = self.color.change_xcolor_to_rgbint(xcolor)

		for one in position:
			range_obj.Borders(one).Color = color
			range_obj.Borders(one).Weight = thickness
			range_obj.Borders(one).LineStyle = style

	def draw_border_line_for_range_as_user_style_02(self, sheet_name, xyxy):
		"""
사용자 정의 스타일 02를 적용하여 영역에 테두리 선을 그림
	(상단/중간/하단 영역별로 서로 다른 선 스타일, 굵기, 색상을 일괄 적용)

	:param sheet_name: (str) 시트 이름, ""은 현재 활성화된 시트
	:param xyxy: (list or str) 영역 주소 (예: "A1:B3" 또는 [r1, c1, r2, c2])
	:return: None
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		line_list_head = [
			["left", "basic", "t-2", "red"],
			["top", "basic", "t-2", "black"],
			["right", "basic", "t-2", "red"],
			["bottom", "basic", "t-2", "black"],
			["inside-h", "basic", "t-2", "black"],
			["inside-v", "basic", "t-2", "black"],
		]
		line_list_body = [
			["left", "basic", "basic", "black"],
			["top", "basic", "basic", "black"],
			["right", "basic", "basic", "black"],
			["bottom", "basic", "basic", "black"],
			["inside-h", "basic", "basic", "black"],
			["inside-v", "basic", "basic", "black"],
		]
		line_list_tail = [
			["left", "basic", "t0", "black"],
			["top", "basic", "t0", "red"],
			["right", "basic", "t0", "red"],
			["bottom", "basic", "basic", "red"],
			["inside-h", "basic", "basic", "red"],
			["inside-v", "basic", "basic", "red"],
		]
		range_head = [x1, y1, x1, y2]
		range_body = [x1 + 1, y1, x2 - 1, y2]
		range_tail = [x2, y1, x2, y2]
		for one in line_list_head:
			self.draw_border_line("", range_head, one)
		for one in line_list_body:
			self.paint_range_line("", range_body, one)
		for one in line_list_tail:
			self.paint_range_line("", range_tail, one)

	def draw_border_line_for_range_at_bottom(self, sheet_name, xyxy, color_name, style, thickness):
		"""
지정한 영역의 하단 테두리 선을 설정함

	:param sheet_name: (str) 시트 이름
	:param xyxy: (list or str) 대상 영역 주소
	:param color_name: (str) 색상 이름 (예: 'red56', '빨강')
	:param style: (str) 선 스타일
	:param thickness: (str/int) 선 두께
	:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.draw_border_line_for_bottom(sheet_name="", xyxy="", line_style="-", thickness="basic", color_name="yel70")
			<object_name>.draw_border_line_for_bottom("", "", "-", thickness="basic", color_name="red50")
			<object_name>.draw_border_line_for_bottom(sheet_name="sht1", xyxy="", line_style="-", thickness="basic", color_name="yel70")
		"""
		self.draw_border_line_for_range(sheet_name, xyxy, "bottom", color_name, style, thickness)

	def draw_border_line_for_range_at_left(self, sheet_name, xyxy, color_name, style, thickness):
		"""
		입력영역의 왼쪽 부분의 선을 긎는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param line_style: (str) 선의 스타일, (점선, 실선등)
		:param thickness: (int) 선의 두께
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.draw_border_line_for_left(sheet_name="", xyxy="", line_style="-", thickness="basic", color_name="yel70")
			<object_name>.draw_border_line_for_left("", "", "-", thickness="basic", color_name="red50")
			<object_name>.draw_border_line_for_left(sheet_name="sht1", xyxy="", line_style="-", thickness="basic", color_name="yel70")
		"""
		self.draw_border_line_for_range(sheet_name, xyxy, "left", color_name, style, thickness)

	def draw_border_line_for_range_at_outline(self, sheet_name, xyxy, color_name, style, thickness):
		"""
		지정한 영역의 외곽 전체 테두리(상, 하, 좌, 우)를 설정함

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param style: (str) 선의 스타일, (점선, 실선등)
		:param thickness: (int) 선의 두께
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.draw_border_line_for_outline(sheet_name="", xyxy="", style="-", thickness="basic", color_name="yel70")
			<object_name>.draw_border_line_for_outline("", "", "-", thickness="basic", color_name="red50")
			<object_name>.draw_border_line_for_outline(sheet_name="sht1", xyxy="", style="-", thickness="basic", color_name="yel70")
		"""

		self.draw_border_line_for_range(sheet_name, xyxy, "o", color_name, style, thickness)

	def draw_border_line_for_range_at_right(self, sheet_name, xyxy, color_name, style, thickness):
		"""
		영역에서 오른쪽 부분의 선을 긎는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param style: (str) 선의 스타일, (점선, 실선등)
		:param thickness: (int) 선의 두께
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.draw_border_line_for_right(sheet_name="", xyxy="", style="-", thickness="basic", color_name="yel70")
			<object_name>.draw_border_line_for_right("", "", "-", thickness="basic", color_name="red50")
			<object_name>.draw_border_line_for_right(sheet_name="sht1", xyxy="", style="-", thickness="basic", color_name="yel70")
		"""
		self.draw_border_line_for_range(sheet_name, xyxy, "right", color_name, style, thickness)

	def draw_border_line_for_range_at_top(self, sheet_name, xyxy, color_name, style, thickness):
		"""
		영역에서 위쪽 부분의 선을 긎는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param style: (str) 선의 스타일, (점선, 실선등)
		:param thickness: (int) 선의 두께
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.draw_border_line_for_top(sheet_name="", xyxy="", style="-", thickness="basic", color_name="yel70")
			<object_name>.draw_border_line_for_top("", "", "-", thickness="basic", color_name="red50")
			<object_name>.draw_border_line_for_top(sheet_name="sht1", xyxy="", style="-", thickness="basic", color_name="yel70")
		"""
		self.draw_border_line_for_range(sheet_name, xyxy, "top", color_name, style, thickness)
		return 123

	def draw_border_line_for_selection_as_user_style_01(self):
		"""
현재 선택된 영역에 대해 사용자 정의 스타일 01(테이블 형식)을 적용하여 선을 그림
	(외곽선, 내부 가로/세로선, 헤더/푸터 구분선을 일괄 적용)

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.draw_border_line_user_style_03_for_selection_()
		"""
		x1, y1, x2, y2 = self.change_any_address_to_xyxy("")
		range_head = [x1, y1, x1, y2]
		range_body = [x1 + 1, y1, x2 - 1, y2]
		range_tail = [x2, y1, x2, y2]
		range_outline = [x1, y1, x2, y2]

		self.draw_border_line_for_range("", range_outline, [7, 8, 9, 10], "bla", "실선", "t1")
		self.draw_border_line_for_range("", range_body, [11], "bla", "실선", "t-1")
		self.draw_border_line_for_range("", range_outline, [12], "bla", ".", "t-1")
		self.draw_border_line_for_range("", range_head, [9], "bla", "실선", "t0")
		self.draw_border_line_for_range("", range_tail, [8], "bla", "실선", "t0")

	def draw_border_xlines(self):
		"""
			현재 인스턴스에 설정된 기본 영역의 내부 가로 테두리 선을 그림
			:return: None
			"""
		self.draw_border_line(["-"])

	def draw_border_xlines_for_range(self, sheet_name, xyxy, color_name, line_style, thickness):
		"""
		영역에서 안쪽 가로 라인의 선을 긎는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param line_style: (str) 선의 스타일, (점선, 실선등)
		:param thickness: (int) 선의 두께
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.draw_xlines(sheet_name="", xyxy="", line_style="-", thickness="basic", color_name="yel70")
			<object_name>.draw_xlines("", "", "-", thickness="basic", color_name="red50")
			<object_name>.draw_xlines(sheet_name="sht1", xyxy="", line_style="-", thickness="basic", color_name="yel70")
		"""

		self.draw_border_line_for_range(sheet_name, xyxy, ["-"], color_name, line_style, thickness)

	def draw_border_ylines(self):
		"""
			현재 인스턴스에 설정된 기본 영역의 내부 세로 테두리 선을 그림
			:return: None
			"""
		self.draw_border_line(["|"])

	def draw_border_ylines_for_range(self, sheet_name, xyxy, color_name, line_style, thickness):
		"""
		영역에서 안쪽 세로 부분의 선을 긎는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param line_style: (str) 선의 스타일, (점선, 실선등)
		:param thickness: (int) 선의 두께
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.draw_ylines_for_range(sheet_name="", xyxy="", line_style="-", thickness="basic", color_name="yel70")
			<object_name>.draw_ylines_for_range("", "", "-", thickness="basic", color_name="red50")
			<object_name>.draw_ylines_for_range(sheet_name="sht1", xyxy="", line_style="-", thickness="basic", color_name="yel70")
		"""
		self.draw_border_line_for_range(sheet_name, xyxy, ["|"], color_name, line_style, thickness)

	def draw_by_cxyxy(self, cxyxy=""):
		"""
			좌표(x1, y1, x2, y2)를 직접 입력받아 해당 위치에 선(Line) 도형을 생성함

			:param cxyxy: (list) [x1, y1, x2, y2] 형태의 좌표 리스트
			:return: 생성된 Shape 객체
			"""
		new_shape_obj = self.sheet_obj.Shapes.AddLine(cxyxy[0], cxyxy[1], cxyxy[2], cxyxy[3])
		return new_shape_obj

	def draw_circle_at_center(self, sheet_name, s_cxy, r, color_name):
		"""
		지정한 중심 좌표를 기준으로 반지름 r인 원을 생성함
		보통원은 사각형을 만든어서 그안에 원을 만드는데, 이것은 중심을 기준으로 원을 만드는 것이다
		s_cxy : s(start, 시작위치), c(coordinate, 좌표), xy(cxy의 뜻으로 좌표축의 x,y 라는 의미)

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param s_cxy:(list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param r: (int) 정수
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.draw_circle_at_center(sheet_name="", s_cxy=[3,7], r=25, color_name="yel70")
			<object_name>.draw_circle_at_center("", [2,3], 25, "yel70")
			<object_name>.draw_circle_at_center(sheet_name="sht1", s_cxy=[3,4], r=25, color_name="yel70")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		center_x = int(s_cxy[0] - r / 2)
		center_y = int(s_cxy[1] - r / 2)

		shape_obj = sheet_obj.Shapes.AddShape(9, center_x, center_y, r, r)
		shape_obj.Fill.ForeColor.RGB = self.color.change_xcolor_to_rgbint(color_name)
		shape_obj.TextFrame2.VerticalAnchor = 3
		shape_obj.TextFrame2.HorizontalAnchor = 2

	def find_word(self, input_value="입력값"):
		"""
			설정된 영역 내에서 특정 단어를 찾아 반복 탐색함

			:param input_value: (str) 찾을 텍스트
			:return: None
			"""
		first_range = self.range_obj.Find(input_value)
		temp_range = first_range
		if first_range != None:
			while 1:
				temp_range = self.range_obj.FindNext(temp_range)
				if temp_range == None or temp_range == first_range.Address:
					break
				else:
					temp_range = temp_range

	def find_word_for_range(self, sheet_name, xyxy, input_value="입력값"):
		"""
		영역안의 글자를 찾는다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (str) 입력으로 들어오는 텍스트
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.find_word_for_range(sheet_name="", xyxy="", input_value="입력값")
			<object_name>.find_word_for_range("", [1,1,3,20],"입력필요")
			<object_name>.find_word_for_range("sht1", [1,1,1,20], "입력필요")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		first_range = range_obj.Find(input_value)
		temp_range = first_range
		if first_range != None:
			while 1:
				temp_range = range_obj.FindNext(temp_range)
				if temp_range == None or temp_range == first_range.Address:
					break
				else:
					temp_range = temp_range

	def font_bold(self):
		"""
			현재 설정된 영역의 폰트를 굵게 설정함
			:return: None
			"""
		self.range_obj.Font.Bold = True

	def font_bold_for_range(self, sheet_name, xyxy):
		"""
		영역의 폰트를 bold로 설정

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_font_bold_for_range(sheet_name="", xyxy="")
			<object_name>.set_font_bold_for_range("sht1", [1,1,3,20])
			<object_name>.set_font_bold_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Font.Bold = True

	def font_color(self, color_name):
		"""
			현재 설정된 영역의 폰트 색상을 변경함

			:param color_name: (str) 색상 이름
			:return: None
			"""
		self.range_obj.Font.Color = self.color.change_xcolor_to_rgbint(color_name)

	def font_color_for_part_of_cell_value(self, xy, from_to, input_font_list):
		"""
			특정 셀 내용 중 지정한 범위(문자 위치)의 폰트 속성(색상, 굵기 등)을 변경함

			:param xy: (list) 셀의 [row, col] 좌표
			:param from_to: (list) 시작 글자 위치와 끝 글자 위치 [start, end]
			:param input_font_list: (list) 적용할 폰트 속성 리스트
			:return: None
			"""
		input_font_list = self.check_input_data(input_font_list)
		range_obj = self.sheet_obj.Cells(xy[0], xy[1])
		ddd = self.range_obj.GetCharacters(from_to[0], from_to[1] - from_to[0])

		checked_font = self.util.check_font_data(input_font_list)

		if "color" in checked_font.keys(): ddd.Font.Color = checked_font["color"]
		if "bold" in checked_font.keys(): ddd.Font.Bold = True
		if "size" in checked_font.keys(): ddd.Font.Size = checked_font["size"]
		if "underline" in checked_font.keys(): ddd.Font.Underline = True

	def font_color_for_part_of_cell_value_for_range(self, sheet_name, xy, from_to=[7, 12], input_font_list=["Arial"]):
		"""
		입력셀의 값중에서 일부분의 폰트색을 칠하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param from_to: (list) 1부터시작하는 셀의 [가로번호, 세로번호]
		:param input_font_list: (list) 1차원의 list형 자료, 폰트명을 나열하는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.font_color_for_part_of_cell_value(sheet_name="", xy=[2, 4], from_to=[7,12], input_font_list=["Arial"])
			<object_name>.font_color_for_part_of_cell_value("", [2, 4], [7,12], ["Arial"])
			<object_name>.font_color_for_part_of_cell_value(sheet_name="sht1", xy=[12,24], from_to=[8,12], input_font_list=["Arial"])
		"""
		input_font_list = self.check_input_data(input_font_list)
		sheet_obj = self.check_sheet_name(sheet_name)
		range_obj = sheet_obj.Cells(xy[0], xy[1])
		ddd = range_obj.GetCharacters(from_to[0], from_to[1] - from_to[0])

		checked_font = self.util.check_font_data(input_font_list)

		if "color" in checked_font.keys(): ddd.Font.Color = checked_font["color"]
		if "bold" in checked_font.keys(): ddd.Font.Bold = True
		if "size" in checked_font.keys(): ddd.Font.Size = checked_font["size"]
		if "underline" in checked_font.keys(): ddd.Font.Underline = True

	def font_color_for_range(self, sheet_name, xyxy, color_name):
		"""
		셀의 폰트 컬러를 xcolor형식으로 입력된 색으로 적용하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.font_color_for_cell(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.font_color_for_cell("sht1", [1,1,12,23], "red23")
			<object_name>.font_color_for_cell("", [3,3,5,7], "gra34")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Font.Color = self.color.change_rgb_to_rgbint(color_name)

	def font_color_for_range_by_rgb(self, sheet_name, xyxy, input_rgb):
		"""
		셀의 폰트 컬러를 rgb형식으로 입력된 색으로 적용하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_rgb: (list)
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.font_color_for_cell_by_rgb(sheet_name="", xyxy="", input_rgb=[102, 234, 133])
			<object_name>.font_color_for_cell_by_rgb("", "", [102, 234, 133])
			<object_name>.font_color_for_cell_by_rgb(sheet_name="sht1", xyxy="", input_rgb=[102, 234, 133])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Font.Color = self.color.change_rgb_to_rgbint(input_rgb)

	def font_common_dic(self, input_list):
		"""
		모듈 전체에서 사용가능한 사전형 자료입니다
		폰트명은 기준을 만들수 없으므로 제외 시켰다

		:param input_list:
		:return:
		Examples
		--------
		.. code-block:: python
			<object_name>.font_common_dic(input_list=[1, "abc", "가나다"])
			<object_name>.font_common_dic([1, "abc", "가나다"])
			<object_name>.font_common_dic([1, "abc", "가나다"])

		"""
		self.font_dic = {
			"bold": False,
			"color": "bla",
			"italic": False,
			"size": 12,
			"strikethrough": False,
			"subscript": False,
			"superscript": False,
			"alpha": False,
			"underline": False,
			"align_v": 2,
			"align_h": 1}

		for one_value in input_list:
			if one_value in ["bold", "진하게"]:
				self.font_dic["bold"] = True
			elif one_value in ["italic", "이탈릭채", "기울게", "이탈릭", "이탤릭", "이태릭"]:
				self.font_dic["italic"] = True
			elif one_value in ["취소", "strikethrough", "취소선", "strike"]:
				self.font_dic["strikethrough"] = True
			elif one_value in ["아래첨자", "subscript"]:
				self.font_dic["subscript"] = True
			elif one_value in ["윗첨자", "superscript", "super"]:
				self.font_dic["superscript"] = True
			elif one_value in ["밑줄", "underline"]:
				self.font_dic["underline"] = True
			elif isinstance(one_value, int):
				self.font_dic["size"] = one_value
			elif isinstance(one_value, float):
				self.font_dic["alpha"] = one_value
			# tintandshade를 이해하기 쉽게 사용하는 목적
			elif one_value in ["middle", "top", "bottom"]:
				# middle =3, top = 1, bottom = 4, default=2
				temp = {"middle": 3, "top": 1, "bottom": 4}
				self.font_dic["align_v"] = temp[one_value]
			elif one_value in ["center", "left"]:
				# None =1, center=2, left=1, default=1
				temp = {"center": 2, "left": 1}
				self.font_dic["align_h"] = temp[one_value]
			else:
				try:
					self.font_dic["color"] = self.color.change_xcolor_to_rgbint(one_value)
				except:
					pass

		return self.font_dic

	def font_for_range_with_dic_style(self, sheet_name, xyxy, input_dic):
		"""
		폰트의 속성을 설정한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_dic: (dic) 사전형으로 입력되는 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_font_with_dic_style(sheet_name="", xyxy="", input_dic = {"key1":1, "line_1":"red", "input_color":"red", "font_bold":1})
			<object_name>.set_font_with_dic_style("", "", {"key1":1, "line_1":"red", "input_color":"red", "font_bold":1})
			<object_name>.set_font_with_dic_style(sheet_name="sht1", xyxy="", input_dic = {"key1":1, "line_2":"red", "input_color1":"red", "font_bold1":1}])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)

		for one in list(input_dic.keys()):
			if isinstance(one, int):
				sheet_obj.Font.Size = input_dic[one]
			elif one in ["bold", "굵게", "찐하게", "진하게"]:
				sheet_obj.Font.Bold = input_dic[one]
			elif one in ["italic", "이태리", "이태리체", "기울기"]:
				sheet_obj.Font.Italic = input_dic[one]
			elif one in ["strikethrough", "취소선", "취소", "통과선" "strike"]:
				sheet_obj.Font.Strikethrough = input_dic[one]
			elif one in ["subscript", "하위첨자", "아래첨자", "아랫첨자", "밑첨자"]:
				sheet_obj.Font.Subscript = input_dic[one]
			elif one in ["superscript", "윗첨자", "위첨자", "웃첨자"]:
				sheet_obj.Font.Superscript = input_dic[one]
			elif one in ["underline", "밑줄"]:
				sheet_obj.Font.Underline = input_dic[one]
			elif one in ["vertical", "ver", "alignv"]:
				ver_value = {"middle": -4108, "top": 1, "bottom": 4, "default": 2, "중간": 3, "위": 1, "아래": 4}
				sheet_obj.VerticalAlignment = ver_value[input_dic[one]]
			elif one in ["horizental", "hor", "alignh"]:
				ver_value = {"middle": -4108, "top": 1, "bottom": 4, "중간": 3, "위": 1, "아래": 4, "default": 2}
				sheet_obj.HorizontalAlignment = ver_value[input_dic[one]]
			elif one in ["color", "색"]:
				sheet_obj.Font.Color = self.color.change_xcolor_to_rgbint(input_dic[one])
			else:
				pass

	def font_for_range_with_setup(self, sheet_name, xyxy, input_list):
		"""
		영역에 적용한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_font_for_range_with_setup(sheet_name="", xyxy="", input_list=[1, "abc", "가나다"])
			<object_name>.set_font_for_range_with_setup("", "", [1, "abc", "가나다"])
			<object_name>.set_font_for_range_with_setup(sheet_name="sht1", xyxy=[1,1,7,10], input_list=[1, "abc", "가나다"])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		if input_list:
			# 아무것도 없으면, 기존의 값을 사용하고, 있으면 새로이 만든다
			if isinstance(input_list, list):
				self.setup_font(input_list)
			elif isinstance(input_list, dict):
				# 만약 사전 형식이면, 기존에 저장된 자료로 생각하고 update한다
				self.varx["font"].update(input_list)

		range_obj.Font.Size = self.varx["font"]["size"]
		range_obj.Font.Bold = self.varx["font"]["bold"]
		range_obj.Font.Italic = self.varx["font"]["italic"]
		range_obj.Font.Name = self.varx["font"]["name"]

		range_obj.Font.Strikethrough = self.varx["font"]["strikethrough"]
		range_obj.Font.Subscript = self.varx["font"]["subscript"]
		range_obj.Font.Superscript = self.varx["font"]["superscript"]
		range_obj.Font.Underline = self.varx["font"]["underline"]
		range_obj.Font.Color = self.varx["font"]["rgb_int"]

	def font_italic(self):
		"""
			현재 설정된 영역의 폰트를 이탤릭(기울임)체로 설정함
			:return: None
			"""
		self.range_obj.Font.Italic = True

	def font_italic_for_range(self, sheet_name, xyxy):
		"""
		영역안의 값에 취소선을 긎는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_font_italic_for_range(sheet_name="", xyxy="")
			<object_name>.set_font_italic_for_range("sht1", [1,1,3,20])
			<object_name>.set_font_italic_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		range_obj.Font.Italic = True

	def font_name(self, input_font_name):
		"""
			현재 설정된 영역의 글꼴 이름을 변경함

			:param input_font_name: (str) 글꼴 명칭 (예: '맑은 고딕', 'Arial')
			:return: None
			"""
		self.range_obj.Font.Name = input_font_name

	def font_name_for_range(self, sheet_name, xyxy, input_font_name="Arial"):
		"""
		글씨체를 설정하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_font_name: (str) 입력으로 들어오는 텍스트
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_font_name_for_range(sheet_name="", xyxy="", input_font_name="Arial")
			<object_name>.set_font_name_for_range("", "", "Arial")
			<object_name>.set_font_name_for_range(sheet_name="sht1", xyxy=[1,1,5,7], input_font_name="Arial")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		range_obj.Font.Name = input_font_name

	def font_partial_value_for_range(self, sheet_name, xy, from_to, input_list):
		"""
		입력셀의 값중에서 일부분의 폰트를 바꾸는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param from_to: (list) 1부터시작하는 셀의 [가로번호, 세로번호]
		:param input_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_font_in_part_of_cell_value(sheet_name="", xy=[2, 4], from_to=[7,12], input_font_list=["Arial"])
			<object_name>.set_font_in_part_of_cell_value("", [2, 4], [7,12], ["Arial"])
			<object_name>.set_font_in_part_of_cell_value(sheet_name="sht1", xy=[12,24], from_to=[8,12], input_font_list=["Arial"])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		range_obj = sheet_obj.Cells(xy[0], xy[1])
		range_obj = range_obj.GetCharacters(from_to[0], from_to[1] - from_to[0])

		if input_list:
			# 아무것도 없으면, 기존의 값을 사용하고, 있으면 새로이 만든다
			if isinstance(input_list, list):
				self.setup_font(input_list)
			elif isinstance(input_list, dict):
				# 만약 사전 형식이면, 기존에 저장된 자료로 생각하고 update한다
				self.varx["font"].update(input_list)
		try:
			range_obj.Font.Size = self.varx["font"]["size"]
			range_obj.Font.Bold = self.varx["font"]["bold"]
			range_obj.Font.Italic = self.varx["font"]["italic"]
			range_obj.Font.Name = self.varx["font"]["name"]

			range_obj.Font.Strikethrough = self.varx["font"]["strikethrough"]
			range_obj.Font.Subscript = self.varx["font"]["subscript"]
			range_obj.Font.Superscript = self.varx["font"]["superscript"]
			range_obj.Font.Underline = self.varx["font"]["underline"]
			range_obj.Font.Color = self.varx["font"]["rgb_int"]
		except:
			pass

	def font_size(self, size):
		if str(size)[0] == "+":
			size_up = 2 * len(size)
			for one in self.range_obj:
				basic_size = one.Font.Size
				one.Font.Size = int(basic_size) + size_up
		elif str(size)[0] == "-":
			size_down = -2 * len(size)
			for one in self.range_obj:
				new_size = one.Font.Size + size_down
				if new_size <= 0:
					one.Font.Size = 3
				else:
					one.Font.Size = new_size
		else:
			self.range_obj.Font.Size = size

	def font_size_for_range(self, sheet_name, xyxy, size="+"):
		"""
		영역에 글씨크기를 설정한다
		2023-07-24 : +-도 가능하게 변경

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param size: (int) 정수, 크기를 나타내는 숫자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_font_size_for_range(sheet_name="", xyxy="", size="+")
			<object_name>.set_font_size_for_range("", [1,1,3,20], "+")
			<object_name>.set_font_size_for_range("sht1", [1,1,1,20], size="+")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		if str(size)[0] == "+":
			size_up = 2 * len(size)
			for one in range_obj:
				basic_size = one.Font.Size
				one.Font.Size = int(basic_size) + size_up
		elif str(size)[0] == "-":
			size_down = -2 * len(size)
			for one in range_obj:
				new_size = one.Font.Size + size_down
				if new_size <= 0:
					one.Font.Size = 3
				else:
					one.Font.Size = new_size
		else:
			range_obj.Font.Size = size

	def font_strikethrough(self):
		"""
			현재 설정된 영역의 폰트에 취소선을 적용함
			:return: None
			"""
		self.range_obj.Font.Strikethrough = True

	def font_strikethrough_for_range(self, sheet_name, xyxy):
		"""
		영역안의 값에 취소선을 긎는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_font_strikethrough_for_range(sheet_name="", xyxy="")
			<object_name>.set_font_strikethrough_for_range("sht1", [1,1,3,20])
			<object_name>.set_font_strikethrough_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		range_obj.Font.Strikethrough = True

	def font_style(self, input_value):
		"""
			현재 영역의 폰트 스타일을 직접 지정함 (예: "Bold Italic")

			:param input_value: (str) 스타일 명칭
			:return: None
			"""
		self.range_obj.Font.Style = input_value

	def font_underline(self):
		"""
			현재 설정된 영역의 폰트에 밑줄을 적용함
			:return: None
			"""
		self.range_obj.Font.Underline = True

	def font_underline_for_range(self, sheet_name, xyxy):
		"""
		영역의 값에 밑줄을 긎는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_font_underline_for_range(sheet_name="", xyxy="")
			<object_name>.set_font_underline_for_range("sht1", [1,1,3,20])
			<object_name>.set_font_underline_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		range_obj.Font.Underline = True

	def font_with_easy_style_for_range(self, sheet_name, xyxy, *input_l1d):
		"""
		폰트의 속성을 설정한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_l1d: {input_l1d}
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_font_with_dic_style(sheet_name="", xyxy="", input_dic = {"key1":1, "line_1":"red", "input_color":"red", "font_bold":1})
			<object_name>.set_font_with_dic_style("", "", {"key1":1, "line_1":"red", "input_color":"red", "font_bold":1})
			<object_name>.set_font_with_dic_style(sheet_name="sht1", xyxy="", input_dic = {"key1":1, "line_2":"red", "input_color1":"red", "font_bold1":1}])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		for one in input_l1d:
			if isinstance(one, int):
				range_obj.Font.Size = one
			elif one in ["bold", "굵게", "찐하게", "진하게"]:
				range_obj.Font.Bold = one
			elif one in ["italic", "이태리", "이태리체", "기울기"]:
				range_obj.Font.Italic = one
			elif one in ["strikethrough", "취소선", "취소", "통과선" "strike"]:
				range_obj.Font.Strikethrough = one
			elif one in ["subscript", "하위첨자", "아래첨자", "아랫첨자", "밑첨자"]:
				range_obj.Font.Subscript = one
			elif one in ["superscript", "윗첨자", "위첨자", "웃첨자"]:
				range_obj.Font.Superscript = one
			elif one in ["underline", "밑줄"]:
				range_obj.Font.Underline = one
			elif one in ["vertical", "ver", "alignv"]:
				ver_value = {"middle": -4108, "top": 1, "bottom": 4, "default": 2, "중간": 3, "위": 1, "아래": 4}
				range_obj.VerticalAlignment = ver_value[one]
			elif one in ["horizental", "hor", "alignh"]:
				ver_value = {"middle": -4108, "top": 1, "bottom": 4, "중간": 3, "위": 1, "아래": 4, "default": 2}
				range_obj.HorizontalAlignment = ver_value[one]
			elif isinstance(one, list):
				range_obj.Font.Color = self.color.change_xcolor_to_rgbint(one)
			else:
				try:
					range_obj.Font.Color = self.color.change_xcolor_to_rgbint(one)
				except:
					pass

	def font_x_align(self, x_align):
		dic_x = {"right": -4152, "middle": -4108, "center": -4108, "left": -4131, "오른쪽": -4152, "중간": 2, "왼쪽": -4131}
		if x_align: self.range_obj.HorizontalAlignment = dic_x[x_align]

	def font_y_align(self, y_align):
		dic_y = {"middle": -4108, "center": -4108, "top": -4160, "bottom": -4107, "low": -4107, "중간": -4108, "위": -4160,
				 "아래": - 4107}
		if y_align: self.range_obj.VerticalAlignment = dic_y[y_align]

	def fore_color_for_chart(self, input_chart_obj, input_rgb):
		"""
		차트의 forecolor를 설정하는 것

		:param input_chart_obj: (object) 객체, 챠트객체
		:param input_rgb: (list), rgb형식
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_fore_color_for_chart(input_chart_obj="object1", input_rgb=[123, 122, 105])
			<object_name>.set_fore_color_for_chart("object1", [123, 122, 105])
			<object_name>.set_fore_color_for_chart(input_chart_obj="object3", input_rgb=[155, 122, 105])
		"""

		input_chart_obj.ChartArea.Format.Fill.ForeColor.RGB = input_rgb

	def format_date_value(self, value):
		"""날짜/시간 타입을 문자열로 변환"""
		if value is None:
			return None

		# pywintypes.TimeType 처리
		try:
			if isinstance(value, pywintypes.TimeType):
				value_str = str(value)
				parts = value_str.split(" ")
				if len(parts) > 1:
					# 시간 부분이 00:00:00이면 날짜만 반환
					if parts[1].startswith("00:00:00"):
						return parts[0]
					else:
						# 타임존 정보 제거
						time_part = parts[1].split("+")[0] if "+" in parts[1] else parts[1]
						return f"{parts[0]} {time_part}"
				return parts[0]
		except:
			pass

		# datetime 타입 처리
		if isinstance(value, datetime.datetime):
			if value.hour == 0 and value.minute == 0 and value.second == 0:
				return value.strftime("%Y-%m-%d")
			return value.strftime("%Y-%m-%d %H:%M:%S")

		# date 타입 처리
		if isinstance(value, datetime.date):
			return value.strftime("%Y-%m-%d")

		# 시간 타입이 클래스명에 포함된 경우 (일반적인 처리)
		if hasattr(value, '__class__') and 'time' in value.__class__.__name__.lower():
			value_str = str(value)
			if '+' in value_str:
				value_str = value_str.split('+')[0]
			if ' 00:00:00' in value_str:
				value_str = value_str.replace(' 00:00:00', '')
			return value_str.strip()

		return value

	def formula_for_range(self, sheet_name, xyxy, input_value="=Now()"):
		"""
		영역에 수식을 넣는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_formula_for_range(sheet_name="", xyxy="", input_value="=Now()")
			<object_name>.set_formula_for_range(("", "", "=Now()")
			<object_name>.set_formula_for_range((sheet_name="sht1", xyxy=[1,1,7,10], input_value="=Now()")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		range_obj.Formula = input_value

	def freeze(self):
		"""
		현재 선택된 영역을 고정시키는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_freeze()
		"""
		self.xlbook.Windows(1).FreezePanes = False
		x1, y1, x2, y2 = self.change_any_address_to_xyxy("")
		if y1 == 0:
			self.select_xline("", x1)
		elif x1 == 0:
			self.select_yline("", y1)
		else:
			self.select_cell("", [x1, y1])
		self.xlbook.Windows(1).FreezePanes = True

	def freeze_pane_by_xy(self, input_xy):
		self.select_sheet()
		self.xlbook.Windows(1).FreezePanes = False
		self.select_xyxy(input_xy)
		self.xlbook.Windows(1).FreezePanes = True

	def freeze_pane_by_xy_for_sheet(self, sheet_name, input_xy):
		"""
		틀고정 : 셀을 기준으로 실행
		선택역역의 왼쪽위를 기준으로 틀고정이 일어난다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_freeze_pane_by_xy(sheet_name="", xy="")
			<object_name>.set_freeze_pane_by_xy("", [1,1])
			<object_name>.set_freeze_pane_by_xy("sht1", [1,20])
		"""
		self.select_sheet(sheet_name)
		self.xlbook.Windows(1).FreezePanes = False
		self.select_cell(sheet_name, input_xy)
		self.xlbook.Windows(1).FreezePanes = True

	def freeze_pane_for_xline(self, input_xno):
		self.select_sheet()
		self.xlbook.Windows(1).FreezePanes = False
		self.select_xxline(input_xno)
		self.xlbook.Windows(1).FreezePanes = True

	def freeze_pane_for_xline_for_sheet(self, sheet_name, input_xno):
		"""
		틀고정 : 가로열을 기준으로 한 것

		선택영역의 왼쪽끝을 기준으로 틀고정이 일어나므로 첫줄을 하고싶으면 2를 넣어야 한다
		만약 1을 넣으면 현재 시트의 셀이 선택된 곳을 기준으로 틀고정이 일어난다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_xno: (int) 정수, x를 나타내는 가로줄의 번호, row의 숫자번호
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_freeze_pane_for_xline(sheet_name="", input_xno=7)
			<object_name>.set_freeze_pane_for_xline("", 7)
			<object_name>.set_freeze_pane_for_xline("sht1", 7)
		"""
		self.select_sheet(sheet_name)
		self.xlbook.Windows(1).FreezePanes = False
		self.select_xline(sheet_name, input_xno)
		self.xlbook.Windows(1).FreezePanes = True

	def freeze_pane_for_yline(self, input_xno):
		self.select_sheet()
		self.xlbook.Windows(1).FreezePanes = False
		self.select_yyline(input_xno)
		self.xlbook.Windows(1).FreezePanes = True

	def freeze_pane_for_yline_for_sheet(self, sheet_name, input_xno):
		"""
		틀고정 : 세로열을 기준으로 한 것
		선택영역의 왼쪽끝을 기준으로 틀고정이 일어나므로 첫줄을 하고싶으면 2를 넣어야 한다
		만약 1을 넣으면 현재 시트의 셀이 선택된 곳을 기준으로 틀고정이 일어난다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_xno: (int) 정수, x를 나타내는 가로줄의 번호, row의 숫자번호
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_freeze_pane_for_yline(sheet_name="", input_xno=7)
			<object_name>.set_freeze_pane_for_yline("", 7)
			<object_name>.set_freeze_pane_for_yline("sht1", 7)
		"""
		self.select_sheet(sheet_name)
		self.xlbook.Windows(1).FreezePanes = False
		self.select_yline(sheet_name, input_xno)
		self.xlbook.Windows(1).FreezePanes = True

	def freeze_pane_off_for_sheet(self, sheet_name):
		"""
		틀고정 해제

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_freeze_pane_off(sheet_name="")
			<object_name>.set_freeze_pane_off("sht1")
			<object_name>.set_freeze_pane_off("")
		"""
		self.select_sheet(sheet_name)
		self.xlbook.Windows(1).FreezePanes = False

	def full_screen(self, fullscreen=1):
		"""
		전체화면으로 보이게 하는 것

		:param fullscreen: (bool) 전체화면을 볼것인지 아닐지 선택하는것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_full_screen(fullscreen=1)
			<object_name>.set_full_screen(1)
		"""
		self.xlapp.DisplayFullScreen = fullscreen

	def get_4_edge_xy_for_range(self, xyxy):
		self.x1, self.y1, self.x2, self.y2 = xyxy
		result = [[self.x1, self.y1], [self.x1, self.y2], [self.x2, self.y2], [self.x2, self.y1]]
		return result

	def get_56color_for_cell(self):
		result = self.range_obj.Interior.ColorIndex
		return result

	def get_5_value_set_for_cell(self, xy):
		one_cell = self.sheet_obj.Cells(xy[0], xy[1])
		result = {}
		result["value"] = one_cell.Value
		result["value2"] = one_cell.Value2
		result["formula"] = one_cell.Formula
		result["formular1c1"] = one_cell.FormulaR1C1
		result["text"] = one_cell.Text
		return result

	def get_activesheet_name(self):
		sheet_name = self.xlapp.ActiveSheet.Name
		return sheet_name

	def get_activeworkbook_obj(self):
		return self.xlapp.ActiveWorkbook

	def get_address(self, option=""):
		if option == "":
			return self.get_address_for_selection()
		elif "used" in option:
			return self.get_address_for_usedrange('')
		elif "con" in option:
			continuous_rng = self.range_obj.CurrentRegion()
			return self.change_any_address_to_xyxy(continuous_rng)

	def get_address_all_empty_cell(self, sheet_name, xyxy):
		"""
		영역안의 빈셀의 주소값을 묶어서 돌려준다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_all_empty_address(sheet_name="", xyxy="")
			<object_name>.get_all_empty_address("sht1", [1,1,3,20])
			<object_name>.get_all_empty_address("", "")
		"""
		result = []
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		l2d = self.read_value_for_range(sheet_name, xyxy)
		for ix, l1d in enumerate(l2d):
			for iy, value in enumerate(l1d):
				if l2d[ix][iy] == "" or l2d[ix][iy] == None:
					result.append([ix + x1, iy + y1])
		return result

	def get_address_at_xy_for_multi_merged_area(self, start_xy, xy_step, input_no):
		"""
		다음번 셀의 주소틀 눙려주는것
		병합이된 셀이 동일하게 연속적으로 있다고 할때, n번째의 셀 주소를 계산하는것

		:param start_xy: (list or str) 셀영역으로 [1,2], ''(현재 선택 영역)로 사용가능
		:param xy_step: (list) [1, 1]의 형태로 나타내는 것
		:param input_no: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_at_xy_for_multi_merged_area(start_xy=[2, 4], xy_step=[1,3], num=2)
			<object_name>.get_address_at_xy_for_multi_merged_area([2, 4], [1,3], 7)
			<object_name>.get_address_at_xy_for_multi_merged_area(start_xy=[12,4], xy_step=[1,7], num=2)
		"""

		mok, namuji = divmod((input_no - 1), xy_step[1])
		new_x = mok * xy_step[0] + start_xy[0]

		new_y = namuji * xy_step[1] + start_xy[1] + 1
		return [new_x, new_y]

	def get_address_for_4_edge_of_range(self, xyxy):
		"""
		좌표를 주면, 맨끝만 나터내는 좌표를 얻는다

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_xyxy_for_4_edge_of_input_range(xyxy="")
			<object_name>.get_xyxy_for_4_edge_of_input_range([1,1,3,20])
		"""
		temp_1 = []
		for x in [xyxy[0], xyxy[2]]:
			temp = []
			for y in range(xyxy[1], xyxy[3] + 1):
				temp.append([x, y])
			temp_1.append(temp)

		temp_2 = []
		for y in [xyxy[1], xyxy[3]]:
			temp = []
			for x in range(xyxy[0], xyxy[2] + 1):
				temp.append([x, y])
			temp_2.append(temp)

		result = [temp_1[0], temp_2[1], temp_1[1], temp_2[0]]
		return result

	def get_address_for_activecell(self):
		"""
		현재 활성화된 셀의 주소를 돌려준다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_for_activecell()
		"""
		return self.change_any_address_to_xyxy(self.xlapp.ActiveCell.Address)

	def get_address_for_all_empty_cell(self):
		result = []
		l2d = self.read()
		for ix, l1d in enumerate(l2d):
			for iy, value in enumerate(l1d):
				if l2d[ix][iy] == "" or l2d[ix][iy] == None:
					result.append([ix + self.x1, iy + self.y1])
		return result

	def get_address_for_all_empty_cell_for_range(self, sheet_name, xyxy):
		"""
		영역안의 빈셀의 주소값을 묶어서 돌려준다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_for_all_empty_cell_for_range(sheet_name="", xyxy="")
			<object_name>.get_address_for_all_empty_cell_for_range("sht1", [1,1,3,20])
		"""
		result = []
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		l2d = self.read_value_for_range(sheet_name, xyxy)
		for ix, l1d in enumerate(l2d):
			for iy, value in enumerate(l1d):
				if l2d[ix][iy] == "" or l2d[ix][iy] == None:
					result.append([ix + x1, iy + y1])
		return result

	def get_address_for_bottom(self, xy):
		return self.get_address_for_bottom_end_at_xy(xy)

	def get_address_for_bottom_end_for_range(self, sheet_name, xy):
		"""
		값이 있는것의 맨 아래쪽 자료를 찾는 것은 이것을 이용하자
		end 는 만약 바로 밑의 자료가 없으면, 있는것이 나타날때까지의 위치를
		그래서 바로밑의 자료가 있는지를 먼저 확인하는 기능을 넣었다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_for_bottom_end_at_xy(sheet_name="", xy="")
			<object_name>.get_address_for_bottom_end_at_xy("", [1,1])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xy)
		cell = self.new_range_obj(sheet_name, [x1, y1])
		one_value = sheet_obj.Cells(x1 + 1, y1).Value
		if one_value:
			down_end = cell.End(-4121)  # xlDown
			x3, y3, x4, y4 = self.change_any_address_to_xyxy(down_end.Address)
			result = [x3, y3]
		else:
			result = [x1, y1]
		return result

	def get_address_for_currentregion_for_range(self, sheet_name, xy):
		"""
		currentregion의 주소를 갖고오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_for_bottom_end_at_xy(sheet_name="", xy="")
			<object_name>.get_address_for_bottom_end_at_xy("", [1,1])
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		address = range_obj.CurrentRegion.Address
		result = self.change_any_address_to_xyxy(address)
		return result

	def get_address_for_end_for_range(self, sheet_name, xy):
		"""
		어떤 셀을 기준으로 값이 연속된 가장 먼 위치를 갖고오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_for_bottom_end_at_xy(sheet_name="", xy="")
			<object_name>.get_address_for_bottom_end_at_xy("", [1,1])
		"""
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xy)
		cell = self.new_range_obj(sheet_name, [x1, y1])
		left_end = cell.End(-4159)  # xIToLeft
		right_end = cell.End(-4161)  # lToRight
		up_end = cell.End(-4162)  # xlUp
		down_end = cell.End(-4121)  # xlDown

		# 각 방향의 끝 지점 주소 출력
		return [left_end.Address, right_end.Address, up_end.Address, down_end.Address]

	def get_address_for_intersect_two_range(self, xyxy1, xyxy2):
		"""
		두개의 영역에서 교차하는 구간을 돌려준다
		만약 교차하는게 없으면 ""을 돌려준다

		:param xyxy1: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param xyxy2: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_for_intersect_two_range(xyxy1=[1,1,12,12], xyxy2=[3,3,5,18])
			<object_name>.get_address_for_intersect_two_range([1,1,12,12], [3,3,5,18])
			<object_name>.get_address_for_intersect_two_range(xyxy1=[3,3,12,12], xyxy2=[5,5,7,18])
		"""
		x11, y11, x12, y12 = self.change_any_address_to_xyxy(xyxy1)
		x21, y21, x22, y22 = self.change_any_address_to_xyxy(xyxy2)
		if x11 == 0:
			x11 = 1
			x12 = 1048576
		if x21 == 0:
			x21 = 1
			x22 = 1048576
		if y11 == 0:
			y11 = 1
			y12 = 16384
		if y21 == 0:
			y21 = 1
			y22 = 16384
		new_range_x = [x11, x21, x12, x22]
		new_range_y = [y11, y21, y12, y22]
		new_range_x.sort()
		new_range_y.sort()
		if x11 <= new_range_x[1] and x12 >= new_range_x[2] and y11 <= new_range_y[1] and y12 >= new_range_y[1]:
			result = [new_range_x[1], new_range_y[1], new_range_x[2], new_range_y[2]]
		else:
			result = "교차점없음"
		return result

	def get_address_for_intersect_with_range_and_input_address(self, xyxy):
		"""
		이름을 좀더 사용하기 쉽도록 만든것

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_for_intersect_with_range_and_input_address(xyxy="")
			<object_name>.get_address_for_intersect_with_range_and_input_address([1,1,3,20])
		"""
		result = self.check_address_with_datas(xyxy, xyxy)
		return result

	def get_address_for_intersect_with_usedrange_for_range(self, sheet_name, xyxy):
		"""
		입력으로 들어온 영역과 전체 사용자 영역이 곂치는 부분을 계산해 주는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_for_intersect_with_usedrange(sheet_name="", xyxy="")
			<object_name>.get_address_for_intersect_with_usedrange("sht1", [1,1,3,20])
			<object_name>.get_address_for_intersect_with_usedrange("", "")
		"""
		used_address = self.get_address_for_usedrange(sheet_name)
		result = self.get_address_for_intersect_two_range(xyxy, used_address)
		return result

	def get_address_for_range(self):
		"""
		현재 선택영역을 xyxy형태의 주소로 돌려주는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_for_range()
		"""
		temp_address = self.xlApp.Selection.Address
		result = self.change_any_address_to_xyxy(temp_address)
		return result

	def get_address_for_range_name(self, sheet_name, range_name):
		"""
		이름영역의 주소값을 갖고오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param range_name: (str) 입력으로 들어오는 텍스트, 영역이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_for_range_name(sheet_name="", range_name="name1")
			<object_name>.get_address_for_range_name("", "name1")
			<object_name>.get_address_for_range_name(sheet_name="sht1", range_name="name1")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		temp = sheet_obj.Range(range_name).Address
		result = self.change_any_address_to_xyxy(temp)
		return result

	def get_address_for_right_end(self, xyxy):
		self.x1, self.y1, self.x2, self.y2 = self.change_any_address_to_xyxy(xyxy)
		return self.y2

	def get_address_for_right_end_n_bottom_from_cell(self, sheet_name, xy):
		"""
		특정셀을 기준으로 연속된 오른쪽과 아래쪽까지의 주소값

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_for_bottom_end_at_xy(sheet_name="", xy="")
			<object_name>.get_address_for_bottom_end_at_xy("", [1,1])
		"""
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xy)
		address_1 = self.move_activecell_to_bottom(sheet_name, [x1, y1])
		address_2 = self.move_activecell_to_rightend(sheet_name, [x1, y1])
		return [address_1, address_2]

	def get_address_for_selection(self):
		"""
		선택된 영역의 주소값을 갖고온다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_for_selection()
		"""
		temp_address = self.xlapp.Selection.Address
		result = self.change_any_address_to_xyxy(temp_address)
		return result

	def get_address_for_usedrange(self, sheet_name):
		"""
		특정시트의 사용된 영역을 갖고오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_for_usedrange(sheet_name="")
			<object_name>.get_address_for_usedrange("sht1")
			<object_name>.get_address_for_usedrange("")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		result = self.change_any_address_to_xyxy(sheet_obj.UsedRange.Address)
		return result

	def get_address_for_xy_for_multi_merged_area(self, start_xy, xy_step, input_no):
		"""
		다음번 셀의 주소틀 눙려주는것
		병합이된 셀이 동일하게 연속적으로 있다고 할때, n번째의 셀 주소를 계산하는것

		:param start_xy: (list or str) 셀영역으로 [1,2], ''(현재 선택 영역)로 사용가능
		:param xy_step: (list) [1, 1]의 형태로 나타내는 것
		:param input_no: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_at_xy_for_multi_merged_area(start_xy=[2, 4], xy_step=[1,3], num=2)
			<object_name>.get_address_at_xy_for_multi_merged_area([2, 4], [1,3], 7)
			<object_name>.get_address_at_xy_for_multi_merged_area(start_xy=[12,4], xy_step=[1,7], num=2)
		"""

		mok, namuji = divmod((input_no - 1), xy_step[1])
		new_x = mok * xy_step[0] + start_xy[0]

		new_y = namuji * xy_step[1] + start_xy[1] + 1
		return [new_x, new_y]

	def get_address_name(self, sheet_name, range_name="name1"):
		"""
		이름영역의 주소값을 갖고오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param range_name: (str) 입력으로 들어오는 텍스트, 영역이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_name(sheet_name="", range_name="name1")
			<object_name>.get_address_name("", "name1")
			<object_name>.get_address_name(sheet_name="sht1", range_name="name1")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		temp = sheet_obj.Range(range_name).Address
		result = self.change_any_address_to_xyxy(temp)
		return result

	def get_cell_obj_for_cell(self, sheet_name, xy):
		"""
		입력 셀의 객체를 만들어서 돌려준다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_cell_obj(sheet_name="", xy=[7,7])
			<object_name>.get_cell_obj("", [3,20])
			<object_name>.get_cell_obj("", [1,20])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		return sheet_obj.Cells(xy[0], xy[1])

	def get_cell_size(self, x, y, excel_cell_start_pxy=[2, 4], sheet_obj="object1", input_factor=2, monitor_dpi=16):
		"""
		모니터에서 특정셀의 픽셀사이즈를 알아내는 것이다

		:param x: (int) 정수
		:param y: (int) 정수
		:param excel_cell_start_pxy: (list) 영역의 첫 셀의 왼쪽윗부분의 픽셀 리스트
		:param sheet_obj: (object) 객체,
		:param input_factor: (int) 숫자형 factor
		:param monitor_dpi: (int) 모니터의 dpi를 나타내는 숫자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_cell_size(x=2, y=3, excel_cell_start_pxy=[2, 4], sheet_obj="object1", input_factor=2, monitor_dpi=16)
			<object_name>.get_cell_size(2, 3, excel_cell_start_pxy=[2, 4], sheet_obj="object1", input_factor=2, monitor_dpi=16)
			<object_name>.get_cell_size(4, 5, excel_cell_start_pxy=[2, 4], sheet_obj="object1", input_factor=2, monitor_dpi=16)
		"""
		cell_target = sheet_obj.Cells(x, y)
		excel_header_width = excel_cell_start_pxy[0]
		excel_header_height = excel_cell_start_pxy[1]
		excel_zoom100 = cell_target.Parent.Parent.Windows(1).Zoom

		x1 = int((cell_target.Left * excel_zoom100 / 100) * (monitor_dpi / 72) / input_factor + excel_header_width)
		y1 = int((cell_target.Top * excel_zoom100 / 100) * (monitor_dpi / 72) / input_factor + excel_header_height)
		x2 = int((cell_target.Width * excel_zoom100 / 100) * (monitor_dpi / 72)) / input_factor + x1
		y2 = int((cell_target.Height * excel_zoom100 / 100) * (monitor_dpi / 72)) / input_factor + y1

		return [x1, y1, x2, y2]

	def get_conditional_formats_for_sheet(self, sheet_name):
		"""
		특정 시트안의 모든 조건부서식을 갖고오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_all_conditional_format_for_sheet(sheet_name="")
			<object_name>.get_all_conditional_format_for_sheet("sht1")
			<object_name>.get_all_conditional_format_for_sheet("")
		"""
		result = []
		sheet_obj = self.check_sheet_name(sheet_name)
		for format_condition in sheet_obj.UsedRange.FormatConditions:
			condition_type = format_condition.Type
			try:
				applies_to = format_condition.AppliesTo.Address
			except:
				applies_to = None

			try:
				formula1 = format_condition.Formula1
			except:
				formula1 = None

			try:
				formula2 = format_condition.Formula2
			except:
				formula2 = None

			try:
				operator = format_condition.Operator
			except:
				operator = None

			interior_color = format_condition.Interior.Color if hasattr(format_condition, 'Interior') else None
			font_color = format_condition.Font.Color if hasattr(format_condition, 'Font') else None
			font_name = format_condition.Font.Name if hasattr(format_condition, 'Font') else None
			font_size = format_condition.Font.Size if hasattr(format_condition, 'Font') else None
			font_bold = format_condition.Font.Bold if hasattr(format_condition, 'Font') else None
			font_italic = format_condition.Font.Italic if hasattr(format_condition, 'Font') else None
			font_underline = format_condition.Font.Underline if hasattr(format_condition, 'Font') else None

			result.append({'Type': condition_type, 'Formula1': formula1, 'Formula2': formula2, 'Operator': operator, 'AppliesTo': applies_to,
						   'InteriorColor': interior_color, 'FontColor': font_color,
						   'FontName': font_name, 'FontSize': font_size, 'FontBold': font_bold, 'FontItalic': font_italic, 'FontUnderline': font_underline})
		return result

	def get_current_path(self):
		"""
		현재 경로를 알아내는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_current_path()
		"""
		return os.getcwd()

	def get_cxy_for_cell(self, sheet_name, xyxy):
		"""
		셀의 픽셀 좌표를 갖고온다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_cxy_for_cell(sheet_name="", xyxy="")
			<object_name>.get_cxy_for_cell("sht1", [1,1,3,20])
			<object_name>.get_cxy_for_cell("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		return [range_obj.Left, range_obj.Top, range_obj.Width, range_obj.Height]

	def get_cxy_for_cell_by_screen_base(self, excel_hwnd=423456, sheet_obj="object1", row=3, col=7):
		"""
		현재 화면을 기준으로 셀의 절대좌표값을 갖고오는 것이다

		:param excel_hwnd: (int) 핸들값, 핸들값
		:param sheet_obj: (object) 객체,
		:param row: (int) 정수
		:param col: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_cxy_for_cell_by_screen_base(excel_hwnd=423456, sheet_obj="object1", row=3, col=7)
			<object_name>.get_cxy_for_cell_by_screen_base(423456, "object1", 3, 7)
			<object_name>.get_cxy_for_cell_by_screen_base(excel_hwnd=423456, sheet_obj="object3", row=2, col=7)
		"""
		# 셀의 좌표와 크기를 가져옵니다
		cell = sheet_obj.Cells(row, col)
		# 엑셀 창의 위치를 가져옵니다
		window_left, window_top, _, _ = self.get_excel_window_rect(excel_hwnd)
		# 엑셀 창의 클라이언트 영역의 좌표를 가져옵니다
		point = wintypes.POINT()
		point.x = 0
		point.y = 0
		ctypes.windll.user32.ClientToScreen(excel_hwnd.ctypes.byref(point))
		client_left = point.x
		client_top = point.y
		# 셀의 화면 좌표를 계산합니다
		screen_left = client_left + cell.Left
		screen_top = client_top + cell.Top
		return screen_left, screen_top, cell.Width, cell.Height

	def get_cxy_for_visible_range(self, excel_obj):
		"""
		현재 화면에 조금이라도 보이는 셀의 주소를 갖고온다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_cxy_for_visible_range(excel_obj=obj1)
			<object_name>.get_cxy_for_visible_range(obj1)
			<object_name>.get_cxy_for_visible_range(excel_obj=obj123)
		"""
		active_window = excel_obj.ActiveWindow
		visible_range = active_window.VisibleRange

		start_row = visible_range.Row
		start_col = visible_range.Column
		end_row = start_row + visible_range.Rows.Count - 1
		end_col = start_col + visible_range.Columns.Count - 1
		return [start_row, start_col, end_row, end_col]

	def get_degree_for_shape(self, sheet_name, shape_no):
		"""
		도형의 각도를 읽는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param shape_no: (int) 정수 이동시킬 도형 이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_degree_for_shape(sheet_name="", shape_no=3)
			<object_name>.get_degree_for_shape("", 7)
			<object_name>.get_degree_for_shape("sht1", 7)
		"""
		shape_obj = self.new_shape_obj(sheet_name, shape_no)
		result = shape_obj.Rotation
		return result

	def get_diagonal_xy(self, xyxy):
		"""
		좌표와 대각선의 방향을 입력받으면, 대각선에 해당하는 셀을 돌려주는것
		좌표를 낮은것 부터 정렬하기이한것 [3, 4, 1, 2] => [1, 2, 3, 4]

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_diagonal_xy(xyxy=[5, 9, 12, 21])
			<object_name>.get_diagonal_xy([5, 9, 12, 21])
			<object_name>.get_diagonal_xy([1,1,5,7])
		"""
		result = []
		if xyxy[0] > xyxy[2]:
			x1, y1, x2, y2 = xyxy[2], xyxy[3], xyxy[0], xyxy[1]
		else:
			x1, y1, x2, y2 = xyxy

		x_height = abs(x2 - x1) + 1
		y_width = abs(y2 - y1) + 1
		step = x_height / y_width
		temp = 0

		if x1 <= x2 and y1 <= y2:
			# \형태의 대각선
			for y in range(1, y_width + 1):
				x = y * step
				if int(x) >= 1:
					final_x = int(x) + x1 - 1
					final_y = int(y) + y1 - 1
					if temp != final_x:
						result.append([final_x, final_y])
						temp = final_x
		else:
			for y in range(y_width, 0, -1):
				x = x_height - y * step

				final_x = int(x) + x1
				final_y = int(y) + y1 - y_width
				temp_no = int(x)

				if temp != final_x:
					temp = final_x
					result.append([final_x, final_y])
		return result

	def get_dpi(self):
		"""
		스크린의 dpi를 읽어오는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_dpi()
		"""
		# Get the screen DPI
		hdc = ctypes.windll.user32.GetDC(0)
		dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
		ctypes.windll.user32.ReleaseDC(0, hdc)
		return dpi

	def get_empty_addresses_for_range(self, sheet_name, xyxy):
		"""
		영역안의 빈셀의 주소값을 묶어서 돌려준다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_all_empty_address_for_range(sheet_name="", xyxy="")
			<object_name>.get_all_empty_address_for_range("sht1", [1,1,3,20])
			<object_name>.get_all_empty_address_for_range("", "")
		"""
		result = []
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		l2d = self.read_value_for_range(sheet_name, xyxy)
		for ix, l1d in enumerate(l2d):
			for iy, value in enumerate(l1d):
				if l2d[ix][iy] == "" or l2d[ix][iy] == None:
					result.append([ix + x1, iy + y1])
		return result

	def get_excel_hwnd(self):
		"""
		엑셀의 핸들값을 갖고오는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_excel_hwnd()
		"""
		return win32gui.FindWindow(None, self.xlapp.Caption)

	def get_excel_obj(self):
		"""
		엑셀프로그램의 객체를 갖고오는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_excel_obj()
		"""
		return self.xlapp

	def get_excel_window_rect(self, input_hwnd=423456, rate=50):
		"""
		엑셀이 현재 보여지는 영역의 사각형의 크기를갖고오는 것

		:param input_hwnd: (int) 핸들값, 핸들값
		:param rate:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_excel_window_rect(input_hwnd=423456, rate=50)
			<object_name>.get_excel_window_rect(423456, 50)
			<object_name>.get_excel_window_rect(input_hwnd=423456, rate=25)
		"""

		class RECT(ctypes.Structure):
			_fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

		# RECT 구조체를 정의합니다
		rect = RECT()
		# GetWindowRect 함수를 사용하여 창의 위치와 크기를 가져옵니다.
		ctypes.windll.user32.GetWindowRect(input_hwnd, ctypes.byref(rect))
		l1, t1, r1, b1 = rect.left, rect.top, rect.right, rect.bottom
		return [int(rect.left / rate), int(rect.top / rate), int(rect.right / rate), int(rect.bottom / rate)]

	def get_filename_for_active_workbook(self):
		"""
		현재 활성화된 엑셀화일의 이름을 갖고읍니다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_filename_for_active_workbook()
		"""
		return self.xlapp.ActiveWorkbook.Name

	def get_filenames_for_opened_workbook(self):
		"""
		모든 열려있는 엑셀화일의 이름을 갖고옵니다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_filenames_for_opened_workbook()
		"""
		return [one.Name for one in self.xlapp.Workbooks]

	def get_filenames_in_folder(self, directory):
		"""
		폴더 안의 화일을 읽어오는것

		:param directory:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_filenames_in_folder_filter_by_extension_name(directory="./")
			<object_name>.get_filenames_in_folder_filter_by_extension_name("./")
		"""
		filenames = os.listdir(directory)
		result = [os.path.join(directory, filename) for filename in filenames]
		return result

	def get_filenames_in_folder_filter_by_extension_name(self, directory="./", filter="pickle"):
		"""
		pickle로 만든 자료를 저장하는것
		변경함,여러 확장자도 사용할수있도록 ["txt", "png"]
		youtil에 있음

		:param directory: (str) 입력으로 들어오는 파일 위치를 나타내는 디렉토리
		:param filter: (str) 필터를 위해서 화일의 속성을 나타내는 끝의 문자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_filenames_in_folder_filter_by_extension_name(directory="./", filter="pickle")
			<object_name>.get_filenames_in_folder_filter_by_extension_name("./", "pickle"])
			<object_name>.get_filenames_in_folder_filter_by_extension_name(directory="./")
		"""
		result = []
		all_files = os.listdir(directory)
		if filter == "+" or filter == "":
			result = all_files
		else:
			for x in all_files:
				if isinstance(filter, list):
					for one in filter:
						if x.endswith("." + one):
							result.append(x)
				elif x.endswith("." + filter):
					result.append(x)
		return result

	def get_font_color(self):
		return self.range_obj.Font.Color

	def get_font_name(self):
		return self.range_obj.Font.Name

	def get_font_name_for_range(self, sheet_name, xyxy):
		"""
		영역에 적용된 글씨체를 갖고오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_font_name_for_range(sheet_name="", xyxy="")
			<object_name>.get_font_name_for_range("sht1", [1,1,3,20])
			<object_name>.get_font_name_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		result = range_obj.Font.Name
		return result

	def get_formula(self):
		result = []

		tup_2d = self.range_obj.Formula
		if isinstance(tup_2d, list) or isinstance(tup_2d, tuple):
			pass
		else:
			tup_2d = [tup_2d]
		for tup_1d in tup_2d:
			temp_list = []
			for value in tup_1d:
				if str(value).startswith("="):
					temp_list.append(value)
				else:
					temp_list.append(None)
			result.append(temp_list)
		return result

	def get_formula_for_range(self, sheet_name, xyxy):
		"""
		선택한 영역의 수식을 읽어오면, 수식이 없는 것은 입력값이 들어가 있다
		그래서, =로시작하는 수식만 남기는 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_formula_for_range(sheet_name="", xyxy="")
			<object_name>.get_formula_for_range("sht1", [1,1,3,20])
			<object_name>.get_formula_for_range("", "")
		"""
		result = []
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		tup_2d = range_obj.Formula
		if isinstance(tup_2d, list) or isinstance(tup_2d, tuple):
			pass
		else:
			tup_2d = [tup_2d]
		for tup_1d in tup_2d:
			temp_list = []
			for value in tup_1d:
				if str(value).startswith("="):
					temp_list.append(value)
				else:
					temp_list.append(None)
			result.append(temp_list)
		return result

	def get_formulas_for_range(self, sheet_name, xyxy):
		"""
		영역안의 모든 수식을 갖고온다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_formulas_for_range(sheet_name="", xyxy="")
			<object_name>.get_formulas_for_range("sht1", [1,1,3,20])
			<object_name>.get_formulas_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		return range_obj.Formula

	def get_general(self):
		"""
		몇가지 엑셀에서 자주사용하는 것들정의
		엑셀의 사용자, 현재의 경로, 화일이름, 현재시트의 이름

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_general()
		"""
		return [self.xlapp.ActiveWorkbook.Name, self.xlapp.UserName, self.xlapp.ActiveWorkbook.ActiveSheet.Name]

	def get_height(self):
		result = self.range_obj.RowHeight
		return result

	def get_height_for_xxline(self, sheet_name, xx_list):
		"""
		연속된 가로줄의 전체 넓이를 갖고 오는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xx_list: (list) 가로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_height_for_xxline(sheet_name="", xx_list=[3,5])
			<object_name>.get_height_for_xxline("", [1,7])
			<object_name>.get_height_for_xxline(sheet_name="sht1", xx_list=[3,5])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		range_obj = sheet_obj.Range(sheet_obj.Cells(xx_list[0], 1), sheet_obj.Cells(xx_list[1], 1))
		result = range_obj.RowHeight
		return result

	def get_information_for_excel(self):
		"""
		몇가지 엑셀에서 자주사용하는 것들정의
		엑셀의 사용자, 현재의 경로, 화일이름, 현재시트의 이름

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_information_for_excel()
		"""
		result = []
		result.append(self.xlapp.ActiveWorkbook.Name)
		result.append(self.xlapp.UserName)
		result.append(self.xlapp.ActiveWorkbook.ActiveSheet.Name)
		return result

	def get_information_for_shape(self, sheet_name, shape_no):
		"""
		시트의 도형번호를 기준으로 어떤 도형의 기본적인 정보를 갖고오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param shape_no: (int) 정수 도형의 번호
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_information_for_shape(sheet_name="", shape_no=3)
			<object_name>.get_information_for_shape("", 7)
			<object_name>.get_information_for_shape("sht1", 7)
		"""
		result = {}
		sheet_obj = self.check_sheet_name(sheet_name)
		if isinstance(shape_no, int):
			shape_no = self.check_shape_name(sheet_name, shape_no)
		shape_obj = sheet_obj.Shapes(shape_no)
		result["title"] = shape_obj.Title
		result["text"] = shape_obj.TextFrame2.TextRange.Characters.Text
		result["xy"] = [shape_obj.TopLeftCell.Row, shape_obj.TopLeftCell.Column]
		result["no"] = shape_no
		result["name"] = shape_obj.Name
		result["rotation"] = shape_obj.Rotation
		result["left"] = shape_obj.Left
		result["top"] = shape_obj.Top
		result["width"] = shape_obj.Width
		result["height"] = shape_obj.Height
		result["pxywh"] = [shape_obj.Left, shape_obj.Top, shape_obj.Width, shape_obj.Height]
		return result

	def get_information_for_workbook(self):
		"""
		워크북에대한 정보들을 갖고오는 것
		몇가지 엑셀에서 자주사용하는 것들정의
		엑셀의 사용자, 현재의 경로, 화일이름, 현재시트의 이름

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_information_for_workbook()
		"""
		return [self.xlapp.ActiveWorkbook.Name, self.xlapp.UserName, self.xlapp.ActiveWorkbook.ActiveSheet.Name]

	def get_max_x_n_y_for_sheet(self):
		"""
		각 엑셀 버전마다 가로, 세로의 크기가 틀리기 때문에 전체를 설정할때를 나타낼려고 합니다
		엑셀에서는 전체 영역을 주소형태로 나타낼때 $1:$1048576와같이 나타내고있읍니다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_max_x_n_y_for_sheet()
		"""
		sheet_obj = self.new_sheet_obj_for_activesheet()
		max_x = sheet_obj.Rows.Count
		max_y = sheet_obj.Columns.Count
		return [max_x, max_y]

	def get_merged_address_list(self):

		result = []

		for x in range(self.x1, self.x2 + 1):
			for y in range(self.y1, self.y2 + 1):
				range_obj = self.sheet_obj.Cells(x, y)

				if self.range_obj.MergeCells:
					self.range_obj.Select()
					ddd = self.get_address_for_selection()
					if not ddd in result:
						result.append(ddd)
		return result

	def get_merged_address_list_for_range(self, sheet_name, xyxy):
		"""
		영역안에 병합된것이 잇으면, 병합된 주소를 리스트형태로 돌려준다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_merged_address_list_for_range(sheet_name="", xyxy="")
			<object_name>.get_merged_address_list_for_range("sht1", [1,1,3,20])
			<object_name>.get_merged_address_list_for_range("", "")
		"""
		result = []
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				range_obj = sheet_obj.Cells(x, y)

				if range_obj.MergeCells:
					range_obj.Select()
					ddd = self.read_address_for_selection()
					if not ddd in result:
						result.append(ddd)
		return result

	def get_missing_num_in_serial_num(self):

		result = []
		set_data = set()
		l2d = self.read_value2()
		max_num = None
		min_num = None
		for l1d in l2d:
			for one in l1d:
				if one:
					one = int(one)
		if max_num == None:
			max_num = one
		if min_num == None:
			min_num = one
		max_num = max(one, max_num)
		min_num = min(one, min_num)
		set_data.add(one)
		for num in range(min_num, max_num + 1):
			if not num in set_data:
				result.append(num)
		return result

	def get_missing_num_in_serial_num_for_range(self, sheet_name, xyxy):
		"""
		선택영역에서 연속된 번호중 빠진것을 찾는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_missing_num_in_serial_num_for_range(sheet_name="", xyxy="")
			<object_name>.get_missing_num_in_serial_num_for_range("sht1", [1,1,3,20])
			<object_name>.get_missing_num_in_serial_num_for_range("", "")
		"""
		result = []
		set_data = set()
		l2d = self.read_value2_for_range(sheet_name, xyxy)
		max_num = None
		min_num = None
		for l1d in l2d:
			for one in l1d:
				if one:
					one = int(one)
		if max_num == None:
			max_num = one
		if min_num == None:
			min_num = one
		max_num = max(one, max_num)
		min_num = min(one, min_num)
		set_data.add(one)
		for num in range(min_num, max_num + 1):
			if not num in set_data:
				result.append(num)
		return result

	def get_multi_range_list_by_valued_cells(self, sheet_name):
		"""
		시트 전체에서 수식을 제외하고, 셀에 값이 있는 영역만 갖고오는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_multi_range_list_by_valued_cells(sheet_name="")
			<object_name>.get_multi_range_list_by_valued_cells("sht1")
			<object_name>.get_multi_range_list_by_valued_cells("")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.Cells.SpecialCells(2).Select()
		myString = self.xlapp.Selection.Address
		return myString

	def get_panthom_link(self):
		names_count = self.xlbook.Names.Count
		result = []
		if names_count > 0:
			for aaa in range(1, names_count + 1):
				name_name = self.xlbook.Names(aaa).Name
				name_range = self.xlbook.Names(aaa)

				if "#ref!" in str(name_range).lower():
					print("found panthom link!!! ===> ", name_name)
					result = True
				else:
					print("normal link, ", name_name)
					result = False
		return result

	def get_path_for_workbook(self):
		"""
		워크북의 경로를 읽어온다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_path_for_workbook()
		"""
		return self.xlbook.Path

	def get_pixel_size_for_cell(self, sheet_name, xyxy):
		"""
		영역의 픽셀값을 4개로 얻어오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_pixel_size_for_cell(sheet_name="", xyxy="")
			<object_name>.get_pixel_size_for_cell("sht1", [1,1,3,20])
			<object_name>.get_pixel_size_for_cell("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		rng_x_coord = range_obj.Left
		rng_y_coord = range_obj.Top
		rng_width = range_obj.Width
		rng_height = range_obj.Height
		return [rng_x_coord, rng_y_coord, rng_width, rng_height]

	def get_program_rect(self, input_hwnd):
		"""
		입력으로 들어오는 핸들값을 가진 프로그램의 사이즈를 갖고오는 것

		:param input_hwnd: (int) 핸들값, 핸들값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_program_rect(input_hwnd = 317856)
			<object_name>.get_program_rect(365356)
			<object_name>.get_program_rect(316546)
		"""
		rect = win32gui.GetWindowRect(input_hwnd)
		return rect

	def get_properties_for_cell(self, sheet_name, xy):
		"""
		셀의 모든 속성을 돌려주는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_properties_for_cell(sheet_name="", xy=[7, 7])
			<object_name>.get_properties_for_cell("", [7, 7])
			<object_name>.get_properties_for_cell(sheet_name="sht1", xy=[7, 7])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		one_cell = sheet_obj.Cells(xy[0], xy[1])
		result = {}
		result["y"] = xy[0]
		result["x"] = xy[1]
		result["value"] = one_cell.Value
		result["value2"] = one_cell.Value2
		result["formula"] = one_cell.Formula
		result["formular1c1"] = one_cell.FormulaR1C1
		result["text"] = one_cell.Text
		result["font_background"] = one_cell.Font.Background
		result["font_bold"] = one_cell.Font.Bold
		result["font_color"] = one_cell.Font.Color
		result["font_colorindex"] = one_cell.Font.ColorIndex
		result["font_creator"] = one_cell.Font.Creator
		result["font_style"] = one_cell.Font.FontStyle
		result["font_italic"] = one_cell.Font.Italic
		result["font_name"] = one_cell.Font.Name
		result["font_size"] = one_cell.Font.Size
		result["font_strikethrough"] = one_cell.Font.Strikethrough
		result["font_subscript"] = one_cell.Font.Subscript
		result["font_superscript"] = one_cell.Font.Superscript
		try:
			result["font_themecolor"] = one_cell.Font.ThemeColor
			result["font_themefont"] = one_cell.Font.ThemeFont
			result["font_tintandshade"] = one_cell.Font.TintAndShade
			result["font_underline"] = one_cell.Font.Underline
			result["memo"] = one_cell.Comment.Text()
		except:
			result["memo"] = ""
		result["background_color"] = one_cell.Interior.Color
		result["background_colorindex"] = one_cell.Interior.ColorIndex
		result["numberformat"] = one_cell.NumberFormat
		# linestyle이 없으면 라인이 없는것으로 생각하고 나머지를 확인하지 않으면서 시간을 줄이는 것이다
		result["line_top_style"] = one_cell.Borders(7).LineStyle
		result["line_top_color"] = one_cell.Borders(7).Color
		result["line_top_colorindex"] = one_cell.Borders(7).ColorIndex
		result["line_top_thick"] = one_cell.Borders(7).Weight
		result["line_top_tintandshade"] = one_cell.Borders(7).TintAndShade
		result["line_bottom_style"] = one_cell.Borders(8).LineStyle
		result["line_bottom_color"] = one_cell.Borders(8).Color
		result["line_bottom_colorindex"] = one_cell.Borders(8).ColorIndex
		result["line_bottom_thick"] = one_cell.Borders(8).Weight
		result["line_bottom_tintandshade"] = one_cell.Borders(8).TintAndShade
		result["line_left_style"] = one_cell.Borders(9).LineStyle
		result["line_left_color"] = one_cell.Borders(9).Color
		result["line_left_colorindex"] = one_cell.Borders(9).ColorIndex
		result["line_left_thick"] = one_cell.Borders(9).Weight
		result["line_left_tintandshade"] = one_cell.Borders(9).TintAndShade
		result["line_right_style"] = one_cell.Borders(10).LineStyle
		result["line_right_color"] = one_cell.Borders(10).Color
		result["line_right_colorindex"] = one_cell.Borders(10).ColorIndex
		result["line_right_thick"] = one_cell.Borders(10).Weight
		result["line_right_tintandshade"] = one_cell.Borders(10).TintAndShade
		result["line_x1_style"] = one_cell.Borders(11).LineStyle
		result["line_x1_color"] = one_cell.Borders(11).Color
		result["line_x1_colorindex"] = one_cell.Borders(11).ColorIndex
		result["line_x1_thick"] = one_cell.Borders(11).Weight
		result["line_x1_tintandshade"] = one_cell.Borders(11).TintAndShade
		result["line_x2_style"] = one_cell.Borders(12).LineStyle
		result["line_x2_color"] = one_cell.Borders(12).Color
		result["line_x2_colorindex"] = one_cell.Borders(12).ColorIndex
		result["line_x2_thick"] = one_cell.Borders(12).Weight
		result["line_x2_tintandshade"] = one_cell.Borders(12).TintAndShade
		return result

	def get_pxy_for_cell(self, x, y, sheet_obj):
		"""
		하나의 셀에대한 그위치의 필셀값을 갖고오는 것

		:param x: (int) 정수
		:param y: (int) 정수
		:param sheet_obj: (object) 객체,
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_pxy_for_cell(x=12, y=11, sheet_obj=obj1)
			<object_name>.get_pxy_for_cell(3, 4, obj1)
			<object_name>.get_pxy_for_cell(x=2, y=7, sheet_obj=obj123)
		"""

		excel_header_width, excel_header_height = self.get_visible_range_window_coordinates()
		cell_target = sheet_obj.Cells(x, y)

		excel_zoom100 = cell_target.Parent.Parent.Windows(1).Zoom
		exce_dpi = self.get_dpi()
		print("dpi는 => ", exce_dpi)

		x1 = (cell_target.Left * excel_zoom100 / 100) * (exce_dpi / 72) + excel_header_width
		y1 = (cell_target.Top * excel_zoom100 / 100) * (exce_dpi / 72) + excel_header_height
		x2 = (cell_target.Width * excel_zoom100 / 100) * (exce_dpi / 72) + x1
		y2 = (cell_target.Height * excel_zoom100 / 100) * (exce_dpi / 72) + y1

		return [x1, abs(y1), x2, abs(y2)]

	def get_pxywh(self):
		return [self.range_obj.Left, self.range_obj.Top, self.range_obj.Width, self.range_obj.Height]

	def get_pxywh_for_range(self, sheet_name, xyxy):
		"""
		영역의 넓이와 높이에 대한 정보를 왼쪽위의 픽셀값과 넓이와 높이로 갖고오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_pxywh(sheet_name="", xyxy="")
			<object_name>.get_pxywh("sht1", [1,1,3,20])
			<object_name>.get_pxywh("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		return [range_obj.Left, range_obj.Top, range_obj.Width, range_obj.Height]

	def get_pxyxy_for_sheet(self, sheet_hwnd):
		"""
		시트의 영역에대한 넓이와 높이에 대한 정보를 왼쪽위의 픽셀값과 오른쪽아래의 픽셀값으로 나타내는 것

		:param sheet_hwnd: (int) 핸들값, 시트의 핸들값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_pxyxy_for_sheet(sheet_hwnd=420689)
			<object_name>.get_pxyxy_for_sheet(420689)
		"""

		class RECT(ctypes.Structure):
			_fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

		client_rect = RECT()
		ctypes.windll.user32.GetClientRect(sheet_hwnd, ctypes.byref(client_rect))
		client_left, client_top, client_right, client_bottom = client_rect.left, client_rect.top, client_rect.right, client_rect.bottom
		left_xy, right_xy = self.client_to_screen(sheet_hwnd, [client_left, client_top, client_right, client_bottom])

		return [left_xy[0], left_xy[1], right_xy[0], right_xy[1]]

	def get_random_xy_set_from_xyxy(self, xyxy="", count_no=1):
		"""
		엑셀영역안에서 랜덤하게 셀주소를 돌려주는것

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param count_no: (int) 정수 입력숫자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_random_xy_set_from_xyxy(xyxy="", count_no=1)
			<object_name>.get_random_xy_set_from_xyxy("", 1)
			<object_name>.get_random_xy_set_from_xyxy(xyxy = [1,1,3,7], count_no=3)
		"""
		result = []
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for no in range(count_no):
			x = random.randint(x1, x2)
			y = random.randint(y1, y2)
			result.append([x, y])
		return result

	def get_range_for_intersect_two_range(self, xyxy1, xyxy2):
		"""
		두 영역의 교집합 영역을 돌려주는 것

		:param xyxy1: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param xyxy2: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_range_for_intersect_two_range(xyxy1=[1,1,30,30], xyxy2=[40,1, 70, 30])
			<object_name>.get_range_for_intersect_two_range([1,1,30,30], [40,1, 70, 30])
			<object_name>.get_range_for_intersect_two_range(xyxy1=[1,1,40,30], xyxy2=[40,1, 80, 30])
		"""
		result = self.get_intersect_address_with_range1_and_range2(xyxy1, xyxy2)
		return result

	def get_range_names(self):
		"""
		현재 활성화된 엑셀화일의 모든 이름영역(range_name)을 갖고오는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_range_names()
		"""
		names_count = self.xlbook.Names.Count
		result = []
		if names_count > 0:
			for aaa in range(1, names_count + 1):
				name_name = self.xlbook.Names(aaa).Name
				name_range = self.xlbook.Names(aaa)
				result.append([aaa, str(name_name), str(name_range)])
		return result

	def get_range_obj_for_range(self, sheet_name, xyxy):
		"""
		range 객체를 영역으로 만드는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_range_obj_for_range(sheet_name="", xyxy="")
			<object_name>.get_range_obj_for_range("sht1", [1,1,3,20])
			<object_name>.get_range_obj_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		if x1 == 0 or x2 == 0:
			start = self.change_num_to_char(y1)
			end = self.change_num_to_char(y2)
			changed_address = str(start) + ":" + str(end)
			range_obj = sheet_obj.Columns(changed_address)
		elif y1 == 0 or y2 == 0:
			start = self.change_char_to_num(x1)
			end = self.change_char_to_num(x2)
			changed_address = str(start) + ":" + str(end)
			range_obj = sheet_obj.Rows(changed_address)
		else:
			range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		return range_obj

	def get_range_obj_for_selection(self):
		"""
		선택한 영역의 range 객체를 갖고오는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_range_obj_for_selection()
		"""
		range_obj = self.xlapp.Selection
		return range_obj.Address

	def get_range_obj_for_xxline(self, sheet_name, xx_list):
		"""
		세로줄의 영역을 range객체로 만드는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xx_list: (list) 가로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_range_obj_for_xxline(sheet_name="", xx_list=[3,5])
			<object_name>.get_range_obj_for_xxline("", [1,7])
			<object_name>.get_range_obj_for_xxline(sheet_name="sht1", xx_list=[3,5])
		"""
		new_x = self.check_xx_address(xx_list)
		sheet_obj = self.check_sheet_name(sheet_name)
		result = sheet_obj.Rows(str(new_x[0]) + ':' + str(new_x[1]))
		return result

	def get_range_obj_for_yyline(self, sheet_name, yy_list):
		"""
		가로줄의 영역을 range객체로 만드는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param yy_list: (list) 세로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_range_obj_for_yyline(sheet_name="", yy_list=[2, 4])
			<object_name>.get_range_obj_for_yyline("", [2, 4])
			<object_name>.get_range_obj_for_yyline("sht1", [3,7])
		"""
		new_y = self.check_yy_address(yy_list)
		sheet_obj = self.check_sheet_name(sheet_name)
		result = sheet_obj.Columns(str(new_y[0]) + ':' + str(new_y[1]))
		return result

	def get_rgb_for_cell(self, sheet_name, xyxy):
		"""
		셀의 배경색을 rgb형식의 리스트로 돌려주는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_rgb_for_cell(sheet_name="", xyxy="")
			<object_name>.get_rgb_for_cell("sht1", [1,1,3,20])
			<object_name>.get_rgb_for_cell("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		rgbint = range_obj.Interior.Color
		result = self.color.change_rgbint_to_rgb(rgbint)
		return result

	def get_rgbint_for_cell(self, sheet_name, xyxy):
		"""
		셀의 배경색을 rgbint로 돌려주는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_rgbint_for_cell(sheet_name="", xyxy="")
			<object_name>.get_rgbint_for_cell("sht1", [1,1,3,20])
			<object_name>.get_rgbint_for_cell("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		result = range_obj.Interior.Color
		return result

	def get_shape_name_by_no(self, sheet_name, shape_no):
		"""
		엑셀화일안에 있는 도형의 번호로 도형의 이름을 갖고오는 것
		번호가 들어오던 이름이 들어오던 도형의 번호를 기준으로 확인해서 돌려주는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param shape_no: (int) 정수 도형의 번호
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_shape_name_by_no(sheet_name="", shape_no=3)
			<object_name>.get_shape_name_by_no("", 7)
			<object_name>.get_shape_name_by_no("sht1", 7)
		"""
		check_dic = {}

		if isinstance(shape_no, int):
			result = shape_no
		else:
			sheet_obj = self.check_sheet_name(sheet_name)
			for index in sheet_obj.Shapes.Count:
				shape_name = sheet_obj.Shapes(index).Name
				check_dic[shape_name] = index
			result = check_dic[shape_no]
		return result

	def get_shape_name_for_sheet_by_index(self, sheet_name, shape_no):
		"""
		번호로 객체의 이름을 갖고오는것
		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param shape_no: (int) 정수 도형의 번호
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_shape_name_for_sheet_by_index(sheet_name="", shape_no=3)
			<object_name>.get_shape_name_for_sheet_by_index("", 7)
			<object_name>.get_shape_name_for_sheet_by_index("sht1", 7)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		result = sheet_obj.Shapes(shape_no).Name
		return result

	def get_shape_names_for_selected_shape(self):
		result = []
		sel_shape_objs = self.xlapp.Selection.ShapeRange
		if sel_shape_objs.Count:
			for one_obj in sel_shape_objs:
				shape_name = one_obj.Name
				result.append(shape_name)
		return result

	def get_shape_names_for_sheet(self, sheet_name):
		"""
		현재 시트의 모든 객체의 이름에 대해서 갖고오는 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_shape_names_for_sheet(sheet_name="")
			<object_name>.get_shape_names_for_sheet("sht1")
			<object_name>.get_shape_names_for_sheet("")
		"""
		result = []
		sheet_obj = self.check_sheet_name(sheet_name)
		shape_ea = sheet_obj.Shapes.Count
		if shape_ea > 0:
			for no in range(shape_ea):
				result.append(sheet_obj.Shapes(no + 1).Name)
		return result

	def get_shape_names_for_workbook(self):
		"""
		엑셀화일안의 모든 그림객체에대한 이름을 갖고온다
		결과 : [시트이름, 그림이름]

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_shape_names_for_workbook()
		"""
		result = []
		sheets_name = self.get_sheet_names()
		for sheet_name in sheets_name:
			shapes_name = self.get_shape_names(sheet_name)
			if shapes_name:
				for shape_name in shapes_name:
					result.append([sheet_name, shape_name])
		return result

	def get_shape_obj_by_name(self, shape_no):
		if isinstance(shape_no, str):
			shape_name = self.get_shape_name_by_no(shape_no)
			shape_obj = self.sheet_obj.Shapes(shape_name)
		elif isinstance(shape_no, int):
			shape_obj = self.sheet_obj.Shapes(shape_no)
		return shape_obj

	def get_shape_obj_by_no(self, shape_no):
		if isinstance(shape_no, str):
			shape_name = self.get_shape_name_by_no(shape_no)
			shape_obj = self.sheet_obj.Shapes(shape_name)
		elif isinstance(shape_no, int):
			shape_obj = self.sheet_obj.Shapes(shape_no)
		return shape_obj

	def get_shape_obj_by_no_or_name(self, sheet_name, shape_no):
		"""
		도형의 번호를 기준으로 도형의 객체를 갖고오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param shape_no: (int) 정수 도형의 번호
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_shape_obj_by_no_or_name(sheet_name="", shape_no=3)
			<object_name>.get_shape_obj_by_no_or_name("", 7)
			<object_name>.get_shape_obj_by_no_or_name("sht1", 7)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)

		if isinstance(shape_no, str):
			shape_name = self.check_shape_name(sheet_name, shape_no)
			shape_obj = sheet_obj.Shapes(shape_name)
		elif isinstance(shape_no, int):
			shape_obj = sheet_obj.Shapes(shape_no)
		return shape_obj

	def get_shapes_name_for_workbook(self):
		"""
		엑셀화일안의 모든 그림객체에대한 이름을 갖고온다

		:return: 결과 : [시트이름, 그림이름]
		Examples
		--------
		.. code-block:: python
			<object_name>.get_shapes_name_for_workbook()
		"""
		result = []
		sheets_name = self.get_sheets_name()
		for sheet_name in sheets_name:
			shapes_name = self.read_shapes_name_for_sheet(sheet_name)
			if shapes_name:
				for shape_name in shapes_name:
					result.append([sheet_name, shape_name])
		return result

	def get_sheet_hwnd(self, excel_hwnd):
		"""
		클라이언트 영역의 핸들 찾기

		:param excel_hwnd: (int) 핸들값, 핸들값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_sheet_hwnd(excel_hwnd=420689)
			<object_name>.get_sheet_hwnd(420689)

		"""
		child_windows = self.enum_child_windows(excel_hwnd)
		client_hwnd = None
		for child in child_windows:
			class_name = win32gui.GetClassName(child)
			if class_name == "EXCEL7":
				client_hwnd = child
				break
		return client_hwnd

	def get_sheet_name_by_position_no(self, input_no):
		"""
		워크시트의 위치번호로 워크시트 이름을 갖고온다

		:param input_no: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_sheet_name_by_position_no(input_no=3)
			<object_name>.get_sheet_name_by_position_no(5)
			<object_name>.get_sheet_name_by_position_no(7)
		"""
		return self.xlbook.Worksheets(input_no).Name

	def get_sheet_names(self):
		"""
		현재 활성화된 엑셀화일의 모든 워크시트의 이름을 읽어온다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_sheets_name()
		"""
		return [self.xlbook.Worksheets(a).Name  for a in range(1, self.xlbook.Worksheets.Count + 1)]

	def get_sheet_names_sort_by_position(self):
		"""
		워크시트의 모든 이름을 위치를 기준으로 정렬해서 돌려준다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_sheet_names_sort_by_position()
		"""
		result = []
		for a in range(1, self.xlbook.Worksheets.Count + 1):
			result.append(self.xlbook.Worksheets(a).Name)
		return result

	def get_sheet_obj_for_activesheet(self):
		"""
		현재 활성화된 시트를 객체형식으로 돌려주는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_sheet_obj_for_activesheet()
		"""
		return self.check_sheet_name("")

	def get_sheets_name(self):
		"""
		현재 활성화된 엑셀화일의 모든 워크시트의 이름을 읽어온다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_sheets_name()
		"""
		return [self.xlbook.Worksheets(a).Name  for a in range(1, self.xlbook.Worksheets.Count + 1)]

	def get_unique_columns_basic(self, input_l2d, input_l1d):
		"""
		input_l2d: 2차원 리스트
		input_l1d: 뽑아낼 열 인덱스 리스트
		"""
		# 1. 특정 열만 추출하여 튜플로 변환 (중복 체크를 위해)
		# 2. set 생성 시 자동으로 중복 제거됨
		unique_set = {tuple(row[i] for i in input_l1d) for row in input_l2d}

		# 3. 결과를 다시 리스트의 리스트 형태로 변환
		return [list(row) for row in unique_set]

	def get_username(self):
		"""
		사용자 이름을 읽어온다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_username()
		"""
		return self.get_username_for_workbook()

	def get_username_for_workbook(self):
		"""
		사용자 이름을 읽어온다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_username_for_workbook()
		"""
		return self.xlapp.UserName

	def get_vba_module_names(self):
		result = []
		for i in self.xlbook.VBProject.VBComponents:
			if i.type in [1, 2, 3]:
				result.append(i.Name)
		return result

	def get_vba_sub_names(self):
		"""
		현재 열려진 엑셀 화일안의 매크로모듈 이름을 찾아서 돌려주는 것
		아래에 1,2,3을 쓴것은 모듈의 종류를 여러가지인데, 해당하는 모듈의 종류이며.
		이것을 하지 않으면 다른 종류의 것들도 돌려주기 때문이다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_all_vba_sub_name()
		"""
		module_name_list = []
		sub_name_list = []

		VBProj = self.xlbook.VBProject

		for i in VBProj.VBComponents:
			if i.type in [1, 2, 3]:
				module_name_list.append(i.Name)

		for i in VBProj.VBComponents:
			num_lines = i.CodeModule.CountOfLines

			for j in range(1, num_lines + 1):

				if 'Sub' in i.CodeModule.Lines(j, 1) and not 'End Sub' in i.CodeModule.Lines(j, 1):
					aaa = i.CodeModule.Lines(j, 1)
					aaa = str(aaa).replace("Sub", "")
					aaa = aaa.split("(")[0]

					sub_name_list.append(aaa.strip())

		return sub_name_list

	def get_visible_range_window_coordinates(self, excel_obj):
		"""
		윈도우 좌표에서 엑셀의 보여지는 영역의 좌표를 갖고오는 것

		:param excel_obj: (object) 객체, 엑셀 객체
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_visible_range_window_coordinates(excel_obj=obj1)
			<object_name>.get_visible_range_window_coordinates(obj1)
			<object_name>.get_visible_range_window_coordinates(excel_obj=obj123)
		"""
		worksheet = excel_obj.ActiveSheet
		window = excel_obj.ActiveWindow

		# VisibleRange의 좌표 가져오기
		top_left_cell = worksheet.Cells(1, 1)
		top_left_x = window.PointsToScreenPixelsX(top_left_cell.Left)
		top_left_y = window.PointsToScreenPixelsY(top_left_cell.Top)
		return [top_left_x, top_left_y]

	def get_width(self):
		result = self.range_obj.ColumnWidth
		return result

	def get_width_of_yyline(self, sheet_name, yy_list):
		"""
		세로줄로만 된 연속된 영역의 넓이를 갖고오는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param yy_list: (list) 세로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_width_of_yyline(sheet_name="", yy_list=[2, 4])
			<object_name>.get_width_of_yyline("", [2, 4])
			<object_name>.get_width_of_yyline("sht1", [3,7])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		range_obj = sheet_obj.Range(sheet_obj.Cells(1, yy_list[0]), sheet_obj.Cells(1, yy_list[1]))
		result = range_obj.ColumnWidth
		return result

	def get_xlines_when_same_yline_with_input_data(self, filter_line, input_value, first_line_is_title_tf):
		l2d = self.read()
		result = []

		if first_line_is_title_tf:
			result.append(l2d[0])

		for l1d in l2d:
			if input_value in l1d[int(filter_line)]:
				result.append(l1d)

		return result

	def get_xlines_when_same_yline_with_input_data_for_range(self, sheet_name, xyxy, filter_line=3, input_value="입력값", first_line_is_title_tf=True):
		"""
		선택한 영역의 특정 y값이 입력값과 같은 x라인들을 돌려 주는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param filter_line: (int) 필터를 할 세로줄의 번호 , column번호
		:param input_value: (any) 입력값
		:param first_line_is_title_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_xlines_when_same_yline_with_input_data_for_range(sheet_name="", xyxy="", filter_line=2, input_value="입력텍스트", first_line_is_title_tf=True)
			<object_name>.get_xlines_when_same_yline_with_input_data_for_range("", "", 4, "입력텍스트", True)
			<object_name>.get_xlines_when_same_yline_with_input_data_for_range(sheet_name="sht1", xyxy=[1,1,5,7], filter_line=2, input_value="입력텍스트", first_line_is_title_tf=True)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		l2d = self.read_value_for_range(sheet_name, xyxy)
		result = []

		if first_line_is_title_tf:
			result.append(l2d[0])

		for l1d in l2d:
			if input_value in l1d[int(filter_line)]:
				result.append(l1d)

		return result

	def get_xy_for_sheet_area(self, sheet_hwnd=423456, rate=50):
		"""
		엑셀안의 시트영역의 픽셀값을 갖고온다

		:param sheet_hwnd: (int) 핸들값, 핸들값
		:param rate:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_xy_for_sheet_area(sheet_hwnd=421234, rate=12)
			<object_name>.get_xy_for_sheet_area(421234, 11)
		"""
		client_rect = RECT()
		ctypes.windll.user32.GetClientRect(sheet_hwnd, ctypes.byref(client_rect))
		left_xy, right_xy = self.client_to_screen(sheet_hwnd, [client_rect.left, client_rect.top, client_rect.right, client_rect.bottom])
		result = [int(left_xy[0] / rate), int(left_xy[1] / rate), int(right_xy[0] / rate), int(right_xy[1] / rate)]
		return result

	def get_xy_list_for_circle(self, r, precious=10, xy=[0, 0]):
		"""
		엑셀을 기준으로, 반지름이 글자를 원으로 계속 이동시키는 것

		:param r: (int) 정수 반지금
		:param precious: (int) 정수 얼마나 정밀하게 할것인지, 1도를 몇번으로 나누어서 계산할것인지

		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_xy_list_for_circle(r=10, precious=10, xy=[0, 0])
			<object_name>.get_xy_list_for_circle(10, 10, [0, 0])
			<object_name>.get_xy_list_for_circle(r=15, precious=10, xy=[0, 0])
		"""
		result = []
		temp = []
		for do_1 in range(1, 5):
			for do_step in range(90 * precious + 1):
				degree = (do_1 * do_step) / precious
				# r을 더하는 이유는 마이너스는 않되므로 x, y측을 이동시키는것
				x = math.cos(degree) * r
				y = math.sin(degree) * r
				new_xy = [int(round(x)), int(round(y))]

				if not new_xy in temp:
					temp.append(new_xy)
		area_1 = []
		area_2 = []
		area_3 = []
		area_4 = []

		for x, y in temp:
			new_x = x + r + 1 + xy[0]
			new_y = y + r + 1 + xy[1]

			if x >= 0 and y >= 0:
				area_1.append([new_x, new_y])
			elif x >= 0 and y < 0:
				area_2.append([new_x, new_y])
			elif x < 0 and y < 0:
				area_3.append([new_x, new_y])
			elif x < 0 and y >= 0:
				area_4.append([new_x, new_y])
		area_1.sort()
		area_1.reverse()
		area_2.sort()
		area_3.sort()
		area_4.sort()
		area_4.reverse()

		result.extend(area_2)
		result.extend(area_1)
		result.extend(area_4)
		result.extend(area_3)
		return result

	def get_xyxy_for_4_edge_of_input_range(self, xyxy):
		"""
		좌표를 주면, 맨끝만 나터내는 좌표를 얻는다

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_xyxy_for_4_edge_of_input_range(xyxy="")
			<object_name>.get_xyxy_for_4_edge_of_input_range([1,1,3,20])
		"""
		temp_1 = []
		for x in [xyxy[0], xyxy[2]]:
			temp = []
			for y in range(xyxy[1], xyxy[3] + 1):
				temp.append([x, y])
			temp_1.append(temp)

		temp_2 = []
		for y in [xyxy[1], xyxy[3]]:
			temp = []
			for x in range(xyxy[0], xyxy[2] + 1):
				temp.append([x, y])
			temp_2.append(temp)

		result = [temp_1[0], temp_2[1], temp_1[1], temp_2[0]]
		return result

	def gridline_off(self, input_tf=False):
		"""
		그리드라인을 없애는것

		:param input_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_gridline_off(input_tf=1)
			<object_name>.set_gridline_off(0)
			<object_name>.set_gridline_off(True)
		"""
		self.xlapp.ActiveWindow.DisplayGridlines = input_tf

	def gridline_on(self, input_tf=True):
		"""
		그리드라인을 나탄게 하는것

		:param input_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_gridline_on(input_tf=1)
			<object_name>.set_gridline_on(0)
			<object_name>.set_gridline_on(True)
		"""
		self.xlapp.ActiveWindow.DisplayGridlines = input_tf

	def gridline_onoff(self, input_tf=""):
		"""
		그리드라인을 껏다 켰다하는 것

		:param input_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_gridline_onoff(input_tf=1)
			<object_name>.set_gridline_onoff(0)
			<object_name>.set_gridline_onoff(True)
		"""
		if input_tf == "":
			if self.xlapp.ActiveWindow.DisplayGridlines == 0:
				self.xlapp.ActiveWindow.DisplayGridlines = 1
			else:
				self.xlapp.ActiveWindow.DisplayGridlines = 0
		else:
			self.xlapp.ActiveWindow.DisplayGridlines = input_tf

	def hide_sheet(self, hide_tf):
		self.sheet_obj.Visible = hide_tf

	def hide_workbook(self):
		self.xlapp.Visible = 0

	def hide_xxline(self, sheet_name, xx_list):
		"""
		x라인의 여러줄 숨기기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xx_list: (list) 가로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.hide_xxline(sheet_name="", xx_list=[3,5])
			<object_name>.hide_xxline("", [1,7])
			<object_name>.hide_xxline(sheet_name="sht1", xx_list=[3,5])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, x2 = self.check_xx_address(xx_list)
		sheet_obj.Rows(str(x1) + ":" + str(x2)).Hidden = True

	def hide_yyline(self, sheet_name, yy_list):
		"""
		y라인의 여러줄 숨기기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xx_list: (list) 가로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.hide_yylines(sheet_name="", yy_list=[3,5])
			<object_name>.hide_yylines("", [1,7])
			<object_name>.hide_yylines(sheet_name="sht1", yy_list=[3,5])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		y1, y2 = self.check_yy_address(yy_list)
		sheet_obj.Columns(str(y1) + ":" + str(y2)).Hidden = True

	def inputbox(self, input_value):
		return self.xlapp.InputBox(input_value)

	def inputbox_for_range(self, input_value):
		r1c1 = self.xlapp.InputBox(input_value, None, None, None, None, None, None, None, 8).Address
		xyxy = self.change_any_address_to_xyxy(r1c1)
		return xyxy

	def insert_chart(self, sheet_name, chart_type, input_pxywh, source_xyxy):
		"""
		챠트를 만드는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_pxywh: (list) [영역중 왼쪽위의 x축의 픽셀번호, 영역중 왼쪽위의 y축의 픽셀번호, 넓이를 픽셀로 계산한것, 높이를 픽셀로 계산한것]
		:param source_xyxy: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_chart_1(sheet_name="", chart_type="type1", input_pxywh=[3,3,10,20], source_xyxy="")
			<object_name>.insert_chart_1("", "type1", [3,3,10,20], "")
			<object_name>.insert_chart_1(sheet_name="sht1", chart_type="type2", input_pxywh=[3,3,10,20], source_xyxy="")
		"""

		chart_type = self.check_chart_style(chart_type)
		sheet_obj = self.check_sheet_name(sheet_name)
		chart_obj = sheet_obj.Chartobjects.Add(input_pxywh)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(source_xyxy)
		r1c1 = self.xyxy2_to_r1c1([x1, y1, x2, y2])
		range_obj = sheet_obj.Range(r1c1)
		chart_obj.SetSourceData(range_obj)
		chart_obj.ChartType = chart_type
		return chart_obj

	def insert_data_input_l2d_for_range(self, sheet_name, xyxy, xy, input_value):
		"""
		엑셀의 2차원자료에서 중간에 값을 넣으면, 자동으로 뒤로 밀어서적용되게 하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param input_value: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_data_input_l2d(sheet_name="", xyxy="", xy=[1,4], input_value="입력값")
			<object_name>.insert_data_input_l2d("", "", [1,4], "입력값")
			<object_name>.insert_data_input_l2d(sheet_name="sht1", xyxy=[1,1,5,7], xy=[1,4], input_value="입력값")
		"""
		input_value = self.check_input_data(input_value)
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		len_x = x2 - x1 + 1
		if isinstance(xy, list):
			insert_position = len_x * xy[0] + xy[1] - 1
		else:
			insert_position = xy - 1
		reverse_l2d = self.read_value_for_range(sheet_name, xyxy)
		l1d = self.util.change_l2d_to_l1d(reverse_l2d)
		l1d.insert(insert_position, input_value)
		result = self.util.change_l1d_to_l2d_group_by_step(l1d, len_x)
		return result

	def insert_sheet(self, sheet_name):
		"""
		시트이름과 함께 시트하나 추가하기
		함수의 공통적인 이름을 위해서 만든것
		메뉴에서 제외

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_sheet(sheet_name="")
			<object_name>.insert_sheet("sht1")
			<object_name>.insert_sheet("")
		"""
		self.insert_sheet_with_name(sheet_name)

	def insert_sheet_with_name(self, sheet_name):
		"""
		시트이름과 함께 시트하나 추가하기
		함수의 공통적인 이름을 위해서 만든것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_sheet_with_name(sheet_name="")
			<object_name>.insert_sheet_with_name("sht1")
			<object_name>.insert_sheet_with_name("")
		"""
		sheets_name = self.get_sheet_names()
		if sheet_name in sheets_name:
			self.util.messagebox("같은 이름의 시트가 있읍니다")
		else:
			self.xlbook.Worksheets.Add()
			if sheet_name:
				old_name = self.xlapp.ActiveSheet.Name
				self.xlbook.Worksheets(old_name).Name = sheet_name

	def insert_text_at_begin_for_number_value(self):
		input_value = ""
		for x in range(self.x1, self.x2 + 1):
			for y in range(self.y1, self.y2 + 1):
				value = self.sheet_obj.Cells(x, y).Value
				if isinstance(value, int) or isinstance(value, float):
					self.sheet_obj.Cells(x, y).Value = input_value + str(value)

	def insert_text_at_begin_for_range_for_number_value(self, sheet_name, xyxy):
		"""
		입력영역의 값중에서 숫자로된 부분의 셀값의 맨 앞부분에 입력된 문자열을 추가하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_text_at_begin_for_range_for_number_value(sheet_name="", xyxy="")
			<object_name>.insert_text_at_begin_for_range_for_number_value("", [1,1,3,20])
			<object_name>.insert_text_at_begin_for_range_for_number_value("sht1", [1,1,1,20])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		input_value = ""
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_obj.Cells(x, y).Value
				if isinstance(value, int) or isinstance(value, float):
					sheet_obj.Cells(x, y).Value = input_value + str(value)

	def insert_text_at_index_position(self, input_index, input_value):
		for x in range(self.x1, self.x2 + 1):
			for y in range(self.y1, self.y2 + 1):
				# 속도를 위해서 사용하는 함수
				one_value = self.sheet_obj.Cells(x, y).Value

				if len(one_value) > input_index:
					changed_value = str(one_value)[:input_index] + input_value + str(one_value)[input_index:]
					self.sheet_obj.Cells(x, y).Value = changed_value

	def insert_text_at_index_position_for_each_cell_for_range(self, sheet_name, xyxy, input_index, input_value):
		"""
		각 셀의 값의 3번째 위치에 어떤 문자를 모두 넣고싶은경우가 있다, 그럴 때 사용하는 목적이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_no: (int) 정수, 입력으로 들어오는 숫자
		:param input_value: (str) 입력으로 들어오는 텍스트
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_text_at_index_position_for_each_cell(sheet_name="", xyxy="", input_index=3, input_value="입력값" )
			<object_name>.insert_text_at_index_position_for_each_cell(sheet_name="sht1", xyxy=[1,1,4,7], input_index=5, input_value="입력값" )
			<object_name>.insert_text_at_index_position_for_each_cell(sheet_name="", xyxy="", input_index=7, input_value="입력값")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				# 속도를 위해서 사용하는 함수
				one_value = sheet_obj.Cells(x, y).Value

				if len(one_value) > input_index:
					changed_value = str(one_value)[:input_index] + input_value + str(one_value)[input_index:]
					sheet_obj.Cells(x, y).Value = changed_value

	def insert_text_at_right_by_xy_step(self, input_value, xy_step):
		for x in range(self.x1, self.x2 + 1):
			if divmod(x, xy_step[0])[1] == 0:
				for y in range(self.y1, self.y2 + 1):
					if divmod(x, xy_step[1])[1] == 0:
						one_value = self.sheet_obj.Cells(x, y).Value
						if one_value == None:
							one_value = ""
						self.sheet_obj.Cells(x, y).Value = one_value + str(input_value)

	def insert_text_for_range_at_left(self, sheet_name, xyxy, input_value, is_text_tf=False):
		"""
		선택한 영역의 왼쪽에 입력한 글자를 추가
		단, 기존의 값이 숫자라도 문자로 만들어서 추가한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (str) 입력으로 들어오는 텍스트
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_text_for_range_at_left(sheet_name="", xyxy="", input_value="입력값", is_text_tf=False)
			<object_name>.insert_text_for_range_at_left("", [1,1,3,20],"입력필요", False)
			<object_name>.insert_text_for_range_at_left("sht1", [1,1,1,20], "입력필요", is_text_tf=False)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = self.read_value_for_cell("", [x, y])

				if is_text_tf and isinstance(value, str):
					sheet_obj.Cells(x, y).Value = input_value + value

	def insert_text_for_range_at_right(self, sheet_name, xyxy, input_value, is_text_tf=False):
		"""
		선택한 영역의 오른쪽에 입력한 글자를 추가
		단, 기존의 값이 숫자라도 문자로 만들어서 추가한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (str) 입력으로 들어오는 텍스트
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_text_for_range_at_right(sheet_name="", xyxy="", input_value="입력값", is_text_tf=False)
			<object_name>.insert_text_for_range_at_right("", [1,1,3,20],"입력필요", False)
			<object_name>.insert_text_for_range_at_right("sht1", [1,1,1,20], "입력필요", is_text_tf=False)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = self.read_value_for_cell("", [x, y])
				if is_text_tf and isinstance(value, str):
					sheet_obj.Cells(x, y).Value = value + input_value

	def insert_text_for_range_at_right_by_xy_step(self, sheet_name, xyxy, input_value, xy_step):
		"""
		영역의 특정 위치에만 기논값 + 입력값으로 만들기
		시작점부터 x,y 번째 셀마다 값을 넣기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (str) 입력으로 들어오는 텍스트
		:param xy_step: (list) [1, 1]의 형태로 나타내는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_text_for_range_at_right_by_xy_step(sheet_name="", xyxy="", input_value="입력값", xy_step=[1, 1])
			<object_name>.insert_text_for_range_at_right_by_xy_step("", "", input_value="입력값", xy_step=[1, 1])
			<object_name>.insert_text_for_range_at_right_by_xy_step(sheet_name="sht1", xyxy=[1,2,4,5], input_value="입력값", xy_step=[1, 1])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			if divmod(x, xy_step[0])[1] == 0:
				for y in range(y1, y2 + 1):
					if divmod(x, xy_step[1])[1] == 0:
						one_value = sheet_obj.Cells(x, y).Value
						if one_value == None:
							one_value = ""
						sheet_obj.Cells(x, y).Value = one_value + str(input_value)

	def insert_vba_module(self, vba_code, macro_name="name1"):
		"""
		텍스트로 만든 매크로 코드를 실행하는 코드이다

		:param vba_code: (str) 입력으로 들어오는 텍스트,
		:param macro_name: (str) 입력으로 들어오는 텍스트,
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_vba_module(vba_code=code_var1, macro_name="name1")
			<object_name>.insert_vba_module(vba_code=code_var1, macro_name="name2"])
			<object_name>.insert_vba_module(vba_code=code_var1, macro_name="name11")
		"""
		new_vba_code = "Sub " + macro_name + "()" + vba_code + "End Sub"
		mod = self.xlbook.VBProject.VBComponents.Add(1)
		mod.CodeModule.AddFromString(new_vba_code)

	def insert_xline_by_step_with_n_lines(self, step_no, line_no):
		step_no = int(step_no)
		add_x = 0
		for no in range(1, self.x2 - self.x1 + 1):
			x = add_x + no
			if divmod(x, step_no)[1] == step_no - 1:
				for _ in range(line_no):
					num_r1 = self.change_char_to_num(x + self.x1)
					self.sheet_obj.Rows(str(num_r1)).Insert(-4121)
					add_x = add_x + 1

	def insert_xline_for_range_by_step(self, sheet_name, xyxy, step_no):
		"""
		영역의 n번째마다 가로열을 추가하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param step_no: (int) 번호, 반복되는 횟수의 번호, step의 의미 : 간격을 두고 값을 쓸때 (예 : 현재 위치를 기준으로 가로로 2칸씩, 세로로 3칸씩 반복되는 위치에 쓸때)
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_xline_for_range_by_step(sheet_name="", xyxy="", step_no=1)
			<object_name>.insert_xline_for_range_by_step("", "", 1)
			<object_name>.insert_xline_for_range_by_step("sht1", "", 5)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		step_no = int(step_no)
		add_x = 0
		for no in range(1, x2 - x1 + 1):
			x = add_x + no
			if divmod(x, step_no)[1] == step_no - 1:
				num_r1 = self.change_char_to_num(x + x1)
				sheet_obj.Rows(str(num_r1)).Insert(-4121)
				add_x = add_x + 1

	def insert_xline_for_range_by_step_with_n_lines(self, sheet_name, xyxy, step_no, line_no):
		"""
		n번째마다 m열을 추가

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param step_no: (int) 번호, 반복되는 횟수의 번호, step의 의미 : 간격을 두고 값을 쓸때 (예 : 현재 위치를 기준으로 가로로 2칸씩, 세로로 3칸씩 반복되는 위치에 쓸때)
		:param line_no: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_xline_for_range_by_step_with_n_lines(sheet_name="", xyxy="", step_no=1, line_no=1)
			<object_name>.insert_xline_for_range_by_step_with_n_lines("", "", 1, 1)
			<object_name>.insert_xline_for_range_by_step_with_n_lines("sht1", "", 5, 3)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		step_no = int(step_no)
		add_x = 0
		for no in range(1, x2 - x1 + 1):
			x = add_x + no
			if divmod(x, step_no)[1] == step_no - 1:
				for _ in range(line_no):
					num_r1 = self.change_char_to_num(x + x1)
					sheet_obj.Rows(str(num_r1)).Insert(-4121)
					add_x = add_x + 1

	def insert_xline_for_sheet(self, sheet_name, input_xno):
		"""
		입력숫자인 가로열의 밑에 한줄삽입하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_xno: (int) 정수, x를 나타내는 가로줄의 번호, row의 숫자번호
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_xline_for_sheet(sheet_name="", input_xno=7)
			<object_name>.insert_xline_for_sheet("", 7)
			<object_name>.insert_xline_for_sheet("sht1", 7)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		num_r1 = self.change_char_to_num(input_xno)
		sheet_obj.Rows(str(num_r1)).Insert(-4121)

	def insert_xline_with_sum_value_for_each_yline(self, input_l2d, xy):
		"""
		선택한 영역의 세로자료들을 다 더해서 제일위의 셀에 다시 넣는것

		:param input_l2d: (list) 2차원의 list형 자료
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_xline_with_sum_value_for_each_yline(input_l2d=[[1, 2], [4, 5]], xy=[3,4])
			<object_name>.insert_xline_with_sum_value_for_each_yline([[1, 2], [4, 5]], [1,2])
			<object_name>.insert_xline_with_sum_value_for_each_yline(input_l2d=[[1, 2], [4, 5]], xy=[7,9])
		"""

		sheet_obj = self.check_sheet_name("")
		input_l2d = self.check_input_data(input_l2d)

		x_len = len(input_l2d)
		y_len = len(input_l2d[0])
		for y in range(y_len):
			temp = ""
			for x in range(x_len):
				sheet_obj.Cells(x + xy[0], y + xy[1]).Value = ""
				if input_l2d[x][y]:
					temp = temp + " " + input_l2d[x][y]
			sheet_obj.Cells(xy[0], y + xy[1]).Value = str(temp).strip()

	def insert_xxline(self, *xx_list):
		if isinstance(xx_list[0], (list, tuple)) and len(xx_list[0]) == 1:
			self.x1 = xx_list[0][0]
			self.x2 = xx_list[0][0]
		elif isinstance(xx_list[0], (list, tuple)) and len(xx_list[0]) == 2:
			self.x1 = xx_list[0][0]
			self.x2 = xx_list[0][1]
		elif isinstance(xx_list[0], int):
			self.x1 = xx_list[0]
			self.x2 = xx_list[0]
		print(self.x1, self.x2)
		self.sheet_obj.Rows(str(self.x1) + ':' + str(self.x2)).Insert(-4121)

	def insert_xxline_for_range(self, sheet_name, xx_list):
		"""
		가로열을 한줄삽입하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xx_list: (list) 가로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_xxline(sheet_name="", xx_list=[3,5])
			<object_name>.insert_xxline("", [1,7])
			<object_name>.insert_xxline(sheet_name="sht1", xx_list=[3,5])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		xx_list = self.check_xx_address(xx_list)
		sheet_obj.Rows(str(xx_list[0]) + ':' + str(xx_list[1])).Insert()

	def insert_yline(self, sheet_name, input_yno):
		"""
		세로행을 한줄삽입하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_yno: (int) 정수, 엑셀의 세로열(column) 번호를 나타내는것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_yline(sheet_name="", input_yno=1)
			<object_name>.insert_yline("", 1)
			<object_name>.insert_yline(sheet_name="sht1", input_yno=5)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		num_r1 = self.change_num_to_char(input_yno)
		sheet_obj.Columns(num_r1).Insert(-4121) # xlShiftToLeft = -4121

	def insert_yline_by_line_nos_l2d(self, input_l2d, no_list):
		"""
		2차원 리스트의 자료에 원하는 가로줄을 삽입하는 것

		:param input_l2d: (list) 2차원의 list형 자료
		:param no_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_ylines_by_line_nos_l2d(input_l2d=[[1, 2], [4, 5]], no_list=[1,2,3,4])
			<object_name>.insert_ylines_by_line_nos_l2d([[1, 2], [4, 5]], [1,2,3,4])
			<object_name>.insert_ylines_by_line_nos_l2d(input_l2d=[[1, 2], [4, 5]], no_list=[7,9,13])
		"""

		input_l2d = self.check_input_data(input_l2d)
		no_list = self.check_input_data(no_list)

		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_l2d)):
				input_l2d[x].insert(int(one), "")
		return input_l2d

	def insert_yline_for_range_by_step(self, sheet_name, xyxy, step_no):
		"""
		insert_range_yline_bystep(sheet_name="", xyxy="", step_no)
		n번째마다 열을 추가하는것
		새로운 가로열을 선택한 영역에 1개씩 추가하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param step_no: (int) 번호, 반복되는 횟수의 번호, step의 의미 : 간격을 두고 값을 쓸때 (예 : 현재 위치를 기준으로 가로로 2칸씩, 세로로 3칸씩 반복되는 위치에 쓸때)
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_yline_for_range_by_step(sheet_name="", xyxy="", step_no=7)
			<object_name>.insert_yline_for_range_by_step("", "", 7)
			<object_name>.insert_yline_for_range_by_step(sheet_name="sht1", xyxy = [1,1,3,7], step_no=7)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		# 일정부분으로 추가되는것을 앞에서부터 적용
		step_no = int(step_no)
		add_y = 0
		for no in range(0, y2 - y1 + 1):
			y = add_y + no
			if divmod(y, step_no)[1] == step_no - 1:
				num_r1 = self.change_num_to_char(y + y1)
				sheet_obj.Columns(num_r1).Insert(-4121)  # xlShiftToLeft = -4121
				add_y = add_y + 1

	def insert_ylines_by_line_nos_l2d(self, input_l2d, no_list):
		"""
		2차원 리스트의 자료에 원하는 가로줄을 삽입하는 것

		:param input_l2d: (list) 2차원의 list형 자료
		:param no_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_ylines_by_line_nos_l2d(input_l2d=[[1, 2], [4, 5]], no_list=[1,2,3,4])
			<object_name>.insert_ylines_by_line_nos_l2d([[1, 2], [4, 5]], [1,2,3,4])
			<object_name>.insert_ylines_by_line_nos_l2d(input_l2d=[[1, 2], [4, 5]], no_list=[7,9,13])
		"""

		input_l2d = self.check_input_data(input_l2d)
		no_list = self.check_input_data(no_list)

		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_l2d)):
				input_l2d[x].insert(int(one), "")
		return input_l2d

	def insert_yyline(self, *yy_list):
		if len(yy_list) == 1 and len(yy_list[0]) == 2:
			self.y1 = yy_list[0][0]
			self.y2 = yy_list[0][1]
		elif len(yy_list) == 1 and len(yy_list[0]) == 1:
			self.y1 = yy_list[0]
			self.y2 = yy_list[0]
		elif len(yy_list) == 2:
			self.y1 = yy_list[0]
			self.y2 = yy_list[1]

		char_y1 = self.change_num_to_char(self.y1)
		char_y2 = self.change_num_to_char(self.y2)

		self.sheet_obj.Column(str(self.y1) + ':' + str(self.y2)).Insert(-4121)  # xlShiftToLeft = -4121

	def insert_yyline_by_line_nos_l2d(self, input_l2d, no_list):
		input_l2d = self.check_input_data(input_l2d)
		no_list = self.check_input_data(no_list)

		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_l2d)):
				input_l2d[x].insert(int(one), "")
		return input_l2d

	def insert_yyline_by_step(self, step_no):
		# 일정부분으로 추가되는것을 앞에서부터 적용
		step_no = int(step_no)
		add_y = 0
		for no in range(0, self.y2 - self.y1 + 1):
			y = add_y + no
			if divmod(y, step_no)[1] == step_no - 1:
				num_r1 = self.change_num_to_char(y + self.y1)
				self.sheet_obj.Columns(num_r1).Insert(-4121)  # xlShiftToLeft = -4121
				add_y = add_y + 1

	def insert_yyline_for_range(self, sheet_name, yy_list):
		"""
		시트에 세로행을 연속된 여러줄 삽입하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param yy_list: (list) 세로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.insert_yyline_for_range(sheet_name="", yy_list=[2, 4])
			<object_name>.insert_yyline_for_range("", [2, 4])
			<object_name>.insert_yyline_for_range("sht1", [3,7])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		if isinstance(yy_list, list) and len(yy_list) == 1:
			x2 = x1 = self.change_num_to_char(yy_list[0])
		elif isinstance(yy_list, list) and len(yy_list) == 2:
			x1 = self.change_num_to_char(yy_list[0])
			x2 = self.change_num_to_char(yy_list[1])
		else:
			x2 = x1 = self.change_num_to_char(yy_list)
		sheet_obj.Columns(str(x1) + ':' + str(x2)).Insert()

	def intersect_address_with_xyxy_and_currentregion(self, sheet_name, xyxy):
		"""
		영역의 첫번째 자료를 기준으로 빈영역과 아닌 영역을 분리하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.intersect_address_with_xyxy_and_currentregion(sheet_name="", xyxy="")
			<object_name>.intersect_address_with_xyxy_and_currentregion("sht1", [1,1,3,20])
			<object_name>.intersect_address_with_xyxy_and_currentregion("", "")
		"""
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		x3, y3, x4, y4 = self.get_address_for_currentregion("", [x1, y1])
		x5, y5, x6, y6 = self.intersect_range1_range2([x1, y1, x2, y2], [x3, y3, x4, y4])
		result1 = [x5, y5, x6, y6]
		if [x5, y5, x6, y6] == [x1, y1, x2, y2]:
			result2 = None
		else:
			result2 = [x1 + (x6 - x5 + 1), y1, x2, y2]
		return [result1, result2]

	def intersect_range1_range2(self, xyxy1, xyxy2):
		"""
		2개 영역이 교차하는 부분에 대한것

		:param xyxy1: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param xyxy2: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.intersect_range1_range2(xyxy1=[1,1,30,30], xyxy2=[40,1, 70, 30])
			<object_name>.intersect_range1_range2([1,1,30,30], [40,1, 70, 30])
			<object_name>.intersect_range1_range2(xyxy1=[1,1,40,30], xyxy2=[40,1, 80, 30])
		"""
		range_1 = self.change_any_address_to_xyxy(xyxy1)
		range_2 = self.change_any_address_to_xyxy(xyxy2)

		x11, y11, x12, y12 = range_1
		x21, y21, x22, y22 = range_2

		if x11 == 0:
			x11 = 1
			x12 = 1048576
		if x21 == 0:
			x21 = 1
			x22 = 1048576
		if y11 == 0:
			y11 = 1
			y12 = 16384
		if y21 == 0:
			y21 = 1
			y22 = 16384

		new_range_x = [x11, x21, x12, x22]
		new_range_y = [y11, y21, y12, y22]

		new_range_x.sort()
		new_range_y.sort()

		if x11 <= new_range_x[1] and x12 >= new_range_x[2] and y11 <= new_range_y[1] and y12 >= new_range_y[1]:
			result = [new_range_x[1], new_range_y[1], new_range_x[2], new_range_y[2]]
		else:
			result = "교차점없음"
		return result

	def is_cell_in_merge(self, sheet_name, xyxy):
		"""
		현재 셀이 merge가 된것인지를 알아 내는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: (bool)
		Examples
		--------
		.. code-block:: python
			<object_name>.is_cell_in_merge(sheet_name="", xyxy="")
			<object_name>.is_cell_in_merge("sht1", [1,1,3,20])
			<object_name>.is_cell_in_merge("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Cells(x1, y1)

		merge_count = range_obj.MergeArea.Cells.Count
		result = False
		if merge_count > 1:
			result = True
		return result

	def is_empty_range(self):
		l2d = self.read()
		if l2d == None:
			return True
		else:
			for l1d in l2d:
				for value in l1d:
					if value == "" or value == None:
						return False
			return True

	def is_empty_sheet(self, sheet_name):
		"""
		시트가 비었는지를 확인하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: (bool)
		Examples
		--------
		.. code-block:: python
			<object_name>.is_empty_sheet(sheet_name="")
			<object_name>.is_empty_sheet("")
			<object_name>.is_empty_sheet("sht1")
		"""
		try:
			sheet_obj = self.check_sheet_name(sheet_name)

			# 1. UsedRange 확인
			used_range = sheet_obj.UsedRange

			# UsedRange의 행/열 개수가 1개인지 확인
			if used_range.Rows.Count != 1 or used_range.Columns.Count != 1:
				return False

			# 2. UsedRange 주소 확인 (A1이어야 함)
			xyxy = self.get_address_for_usedrange(sheet_name)
			if xyxy != [1, 1, 1, 1]:
				return False

			# 3. A1 셀의 값 확인
			one_value = sheet_obj.Cells(1, 1).Value

			# None, 빈 문자열, 공백만 있는 경우 모두 빈 것으로 간주
			if one_value is None:
				return True
			elif isinstance(one_value, str) and one_value.strip() == "":
				return True
			else:
				return False

		except Exception as e:
			print(f"✗ is_empty_sheet 오류: {str(e)}")
			return False

	def is_empty_values_for_range(self, sheet_name, xyxy):
		"""
		값이 모두 비었을때는 True를 돌려주고 아닌경우는 False를 돌려준다
		여기는 기본으로 ""일때는 usedrange의 주소를 갖고온다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: (bool)
		Examples
		--------
		.. code-block:: python
			<object_name>.is_all_empty_value_for_range(sheet_name="", xyxy="")
			<object_name>.is_all_empty_value_for_range("sht1", [1,1,3,20])
			<object_name>.is_all_empty_value_for_range("", "")
		"""
		if xyxy == "":
			xyxy = self.read_address_for_usedrange(sheet_name)
		l2d = self.read_value_for_range(sheet_name, xyxy)
		if l2d == None:
			return True
		else:
			for l1d in l2d:
				for value in l1d:
					if value == "" or value == None:
						return False
			return True

	def is_empty_xline(self, sheet_name, input_xno):
		"""
		열전체가 빈 것인지 확인해서 돌려준다
		현재의 기능은 한줄만 가능하도록 하였다
		다음엔 영역이 가능하도록 하여야 겠다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_xno: (int) 정수, x를 나타내는 가로줄의 번호, row의 숫자번호
		:return: (bool)
		Examples
		--------
		.. code-block:: python
			<object_name>.is_empty_xline(sheet_name="", input_xno=7)
			<object_name>.is_empty_xline("", 7)
			<object_name>.is_empty_xline("sht1", 7)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		result = self.xlapp.WorksheetFunction.CountA(sheet_obj.Rows(input_xno).EntireRow)
		return result

	def is_empty_yline(self, input_yno):
		"""
		입력한 세로 한줄이 전체가 비어있는지 확인하는 것

		:param input_yno: (int) 정수, 엑셀의 세로열(column) 번호를 나타내는것
		:return: (bool)
		Examples
		--------
		.. code-block:: python
			<object_name>.is_empty_yline(input_yno=2)
			<object_name>.is_empty_yline(2)
			<object_name>.is_empty_yline(7)
		"""
		y1 = self.change_char_to_num(input_yno)
		result = self.xlbook.WorksheetFunction.CountA(self.varx["sheet"].Columns(y1).EntireColumn)
		return result

	def is_file_in_folder(self, path="D:\\test", filename="save_file.py"):
		"""
		폴더안에 파일이 있는지 확인하는 것

		:param path: (str) 입력으로 들어오는 텍스트, 경로를 나타내는 것
		:param filename: (str) 화일의 이름을 나타내는 문자열
		:return: (bool)
		Examples
		--------
		.. code-block:: python
			<object_name>.is_file_in_folder(path="D:\\test", filename="save_file.py")
			<object_name>.is_file_in_folder("D:\\test", "save_file.py")
		"""
		result = ""
		if path == "":
			path = "C:/Users/Administrator/Documents"
		filenames = self.util.get_all_filename_in_folder(path)

		if filename in filenames:
			result = True
		return result

	def is_match_with_xre_for_input_value(self, input_xre, input_value):
		"""
		입력값이 input_xre의 정규표현식의 내용이 들어가 있는지 확인하는 것

		:param input_xre: (str) xre형식의 문자열
		:param input_value: (str) 입력으로 들어오는 텍스트
		:return: (bool)
		Examples
		--------
		.. code-block:: python
			<object_name>.is_match_with_xre_for_input_value(input_xre="[시작:처음][영어:1~4][한글:3~10]", input_value="입력값")
			<object_name>.is_match_with_xre_for_input_value("[시작:처음][영어:1~4][한글:3~10]", "입력값2")
			<object_name>.is_match_with_xre_for_input_value(input_xre="[시작:처음][영어:1~4][한글:3~10]", input_value="입력값3")
		"""
		# resql = self.rex.change_xsql_to_resql(input_xre)
		result = self.rex.search_all_by_xsql(input_xre, input_value)
		if result == []:
			output_text = False
		else:
			output_text = True
		return output_text

	def is_merged_cell(self):
		merge_count = self.range_obj.MergeArea.Cells.Count
		result = False
		if merge_count > 1:
			result = True
		return result

	def is_range_name(self, range_name="name1"):
		"""
		이름영역의 하나인지 아닌지 확인하는 것

		:param range_name: (str) 입력으로 들어오는 텍스트, 영역이름
		:return: (bool)
		Examples
		--------
		.. code-block:: python
			<object_name>.is_range_name(range_name="영역이름1")
			<object_name>.is_range_name("영역이름1")
			<object_name>.is_range_name("영역이름123")
		"""

		result = False
		all_range_name = self.get_range_names()
		if range_name in all_range_name:
			result = True
		return result

	def is_sheet_name(self, sheet_name):
		"""
		입력받은 시트의 이름이 현재 워크북의 이름중하나인지 확인해 보는것
		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: (bool)
		Examples
		--------
		.. code-block:: python
			<object_name>.is_sheet_name(sheet_name="")
			<object_name>.is_sheet_name("sht1")
			<object_name>.is_sheet_name("")
		"""
		result = False
		sheets_name = self.get_sheets_name()
		if sheet_name in sheets_name:
			result = True
		return result

	def lock_sheet_with_password(self, sheet_name):
		"""
		암호걸기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.lock_sheet_with_password(sheet_name="")
			<object_name>.lock_sheet_with_password("sht1")
			<object_name>.lock_sheet_with_password("")
		"""

		source_letter = "1234567890"
		repeat_no = 4
		count = 0
		for a in itertools.product(source_letter, repeat=repeat_no):
			count += 1
			temp_pwd = ("".os.path.join(map(str, a)))
			try:
				self.set_sheet_lock_off(sheet_name, temp_pwd)
			except:
				pass
			else:
				break

	def make_dic_for_input_value_for_each_word_as_count_vs_word(self, input_value):
		"""
		입력으로 들어온 텍스트를 공백으로 분리해서, 단어의 형태로 만들어서
		각 단어들의 갯수를 사전형식으로 만드는 것

		:param input_value: (str) 입력으로 들어오는 텍스트
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.make_dic_for_input_value_for_each_word_as_count_vs_word(input_value="입력글자1")
			<object_name>.make_dic_for_input_value_for_each_word_as_count_vs_word("입력문자들")
			<object_name>.make_dic_for_input_value_for_each_word_as_count_vs_word("입력으로 들어오는 문자")
		"""
		input_value = input_value.replace(" ", "")
		input_value = input_value.upper()
		result = {}
		for one_letter in input_value:
			if one_letter in list(result.keys()):
				result[one_letter] = result[one_letter] + 1
			else:
				result[one_letter] = 1
		return result

	def make_dict_by_first_value(self):
		result = {}
		l2d = self.read()
		l2d = self.util.change_tuple_2d_to_l2d(l2d)

		l2d_changed = self.util.delete_empty_xline_in_l2d(l2d)
		for l1d in l2d_changed:
			result[l1d[0]] = list(l1d)
		return result

	def make_dict_by_first_value_for_range(self, sheet_name, xyxy):
		"""
		맨앞의 글자를 키로 사용해서, 2차원자료를 사전형식으로 만드는 것
		퀴즈같은 문제를 만들때, 속도도 빠르게 하면서, 사용했던것을 다시 안물러 오도록 하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.make_dict_by_first_value_for_range(sheet_name="", xyxy="")
			<object_name>.make_dict_by_first_value_for_range("sht1", [1,1,3,20])
			<object_name>.make_dict_by_first_value_for_range("", "")
		"""
		result = {}
		l2d = self.read_value_for_range(sheet_name, xyxy)
		l2d = self.util.change_tuple_2d_to_l2d(l2d)

		l2d_changed = self.util.delete_empty_xline_in_l2d(l2d)
		for l1d in l2d_changed:
			result[l1d[0]] = list(l1d)
		return result

	def make_l2d_data(self):
		"""
		현재 선택된 자료들을 리스트형태로 만드는 것
		:return:
		"""
		l2d = self.read_range()
		self.new_sheet()
		self.write_value_for_cell("", [1,1], "[")
		for ix, l1d in enumerate(l2d[:-1]):
			self.write_value_for_cell("", [ix+2, 1], str(l1d)+",")
		self.write_value_for_cell("", [len(l2d)+1, 1], str(l2d[-1]) + ",")
		self.write_value_for_cell("", [len(l2d)+2, 1], "]")

	def make_line_for_splitted_data(self, xyxy, union_char="#"):
		"""
		앞에 숫자를 기준으로 옆줄의 자료를 합치는것
		맨앞의 자료 1줄만 합친다

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param union_char: (str) 합칠때 사용할 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.make_line_for_splitted_data(xyxy="", union_char="#")
			<object_name>.make_line_for_splitted_data("", "#")
			<object_name>.make_line_for_splitted_data(xyxy=[1,1,5,7], union_char="#")
		"""
		sheet_obj = self.check_sheet_name("")
		temp = ""
		old_x = xyxy[0]
		for x in range(xyxy[0], xyxy[2] + 1):
			gijun_data = self.read_value_for_cell("", [x, xyxy[1]])
			value = self.read_value_for_cell("", [x, xyxy[1] + 1])

			if gijun_data:
				sheet_obj.Cells(old_x, xyxy[1] + 2).Value = temp[:-len(union_char)]
				temp = value + union_char
				old_x = x
			else:
				temp = temp + value + union_char
		sheet_obj.Cells(old_x, xyxy[1] + 2).Value = temp[:-len(union_char)]

	def make_many_excel_file_group_for_yline_value_for_range(self, sheet_name, xyxy, base_yline_no=3, filename="D:\\__test\\save_file_"):
		"""
		어떤 시트의 특정영역의 자료중에서 n번째 열을 기준으로 같은것끼리 정렬을 해서
		각 그룹별로 새로운 파일을 만들어서 저장하는것
		단, 아래의 코드에는 서식을 함께 사용하기위해서 서식복사를 넣었다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param base_yline_no: (int) 1부터시작하는 세로줄의 column번호
		:param filename: (str) 화일의 이름을 나타내는 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.make_many_excel_file_group_for_yline_value_for_range(sheet_name="", xyxy="", base_yline_no=3, filename="D:\\__test\\save_file_")
			<object_name>.make_many_excel_file_group_for_yline_value_for_range("", "", 3, "D:\\__test\\save_file_")
			<object_name>.make_many_excel_file_group_for_yline_value_for_range(sheet_name="sht1", xyxy="", base_yline_no=3, filename="D:\\__test\\save_file_")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		l2d = self.read_value_for_range(sheet_name, [x1, y1, x2, y2])
		l2d_group = self.util.group_l2d_by_index(l2d, base_yline_no - 1)
		no = 0
		for index in range(len(l2d_group[1:])):
			self.copy_range(sheet_name, [x1, y1, x2, y2])
			# 한번 붙여넣기를 하면 없어져서, 계속 해야한다
			no = no + 1
			xl2 = xy_excel("new")
			xl2.paste_range_format_only("", [1, 1])
			xl2.write_l1d_from_cell("", [1, 1], l2d[0])
			xl2.write_l2d_from_cell("", [1, 1], l2d_group[index + 1])
			xl2.save(filename + str(no) + ".xlsx")
			xl2.close()

	def make_one_text_for_range_with_chain_char(self, sheet_name, xyxy, chain_char="tab"):
		"""
		엑셀의 영역을 각 값들을 어떤 문자로 다 연결해서, 하나의 텍스트로 바꿔주는 것
		기본으로 탭으로 연결해서 만들어 준다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param chain_char: (str) 연결하는 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.make_one_text_for_range_with_chain_char(sheet_name="", xyxy="", chain_char="-")
			<object_name>.make_one_text_for_range_with_chain_char("", [1,1,3,20], "-")
			<object_name>.make_one_text_for_range_with_chain_char("sht1", [1,1,1,20], "-")
		"""
		l2d = self.read_value_for_range(sheet_name, xyxy)
		result = self.util.change_l2d_to_text_with_chain_word(l2d, chain_char)
		return result

	def make_ppt_table_from_xl_data(self):
		"""
		엑셀의 테이블 자료가 잘 복사가 않되는것 같아서, 아예 하나를 만들어 보았다
		엑셀의 선택한 영역의 테이블 자료를 자동으로 파워포인트의 테이블 형식으로 만드는 것이다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.make_ppt_table_from_xl_data()
		"""

		activesheet_name = self.get_activesheet_name()
		[x1, y1, x2, y2] = self.get_address_for_selection()

		Application = win32com.client.Dispatch("Powerpoint.Application")
		Application.Visible = True
		active_ppt = Application.Activepresentation
		slide_no = active_ppt.Slides.Count + 1

		new_slide = active_ppt.Slides.Add(slide_no, 12)
		new_table = active_ppt.Slides(slide_no).Shapes.AddTable(x2 - x1 + 1, y2 - y1 + 1)
		shape_no = active_ppt.Slides(slide_no).Shapes.Count

		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				value = self.read_value_for_cell(activesheet_name, [x, y])
				active_ppt.Slides(slide_no).Shapes(shape_no).Table.Cell(x - x1 + 1,
																			  y - y1 + 1).Shape.TextFrame.TextRange.Text = value

	def make_ppt_table_from_xl_data_ver2(self):
		"""
		엑셀의 테이블 자료가 잘 복사가 않되는것 같아서, 아예 하나를 만들어 보았다
		엑셀의 선택한 영역의 테이블 자료를 자동으로 파워포인트의 테이블 형식으로 만드는 것이다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.make_ppt_table_from_xl_data_ver2()
		"""
		activesheet_name = self.get_sheet_name_for_activesheet()
		[x1, y1, x2, y2] = self.get_address_for_selection()

		Application = win32com.client.Dispatch("Powerpoint.Application")
		Application.Visible = True
		active_ppt = Application.Activepresentation
		slide_no = active_ppt.Slides.Count + 1

		new_slide = active_ppt.Slides.Add(slide_no, 12)
		new_table = active_ppt.Slides(slide_no).Shapes.AddTable(x2 - x1 + 1, y2 - y1 + 1)
		shape_no = active_ppt.Slides(slide_no).Shapes.Count

		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				value = self.read_value_for_cell(activesheet_name, [x, y])
				active_ppt.Slides(slide_no).Shapes(shape_no).Table.Cell(x - x1 + 1,
																			  y - y1 + 1).Shape.TextFrame.TextRange.Text = value

	def make_print_page(self, sheet_name, input_l2d, line_list, start_xy, size_xy, y_line=2, position=3):
		"""
		input_l2d, 2차원의 기본자료들
		2차원의 자료에서 출력하는 자료들만 순서대로 골라서 새로 만드는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_l2d: (list) 2차원의 list형 자료
		:param line_list: (list) 가로줄을 나타내는 숫자, [1,2,3], 각 라인에서 출력이 될 자료
		:param start_xy: (list or str) 셀영역으로 [1,2], ''(현재 선택 영역)로 사용가능, 첫번째로 시작될 자료의 위치
		:param size_xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함, [7,9], 하나가 출력되는 영역의 크기
		:param y_line: (int) 1부터 시작하는 세로를 나타내는 column의 숫자, 2, 한페이지에 몇줄을 출력할것인지
		:param position: (str) 입력으로 들어오는 텍스트, 위치를 나타내는 문자, [1,31,[4,5],[7,9]], 한줄의 출력되는 위치, line_list의 갯수와 같아야 한다
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.make_print_page(sheet_name="", input_l2d=[[1, 2], [4, 5]], line_list=[1,2,3], start_xy=[1,1], size_xy=[2, 4], y_line=2, position=3)
			<object_name>.make_print_page(sheet_name="sht1", input_l2d=[[1, 2], [4, 5]], line_list=[1,2,3], start_xy=[2,1], size_xy=[1,4], y_line=2, position=3)
			<object_name>.make_print_page(sheet_name="sht2", input_l2d=[[1,2,3]], line_list=[,2,3], start_xy=[1,1], size_xy=[2, 4], y_line=2, position=3)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		input_l2d = self.check_input_data(input_l2d)
		changed_input_l2d = self.pick_ylines_at_l2d(input_l2d, line_list)  # 1
		new_start_x = start_xy[0]
		new_start_y = start_xy[1]
		for index, l1d in enumerate(changed_input_l2d):
			mok, namuji = divmod(index, y_line)
			new_start_x = new_start_x + mok * size_xy[0]
			new_start_y = new_start_y + namuji * size_xy[1]
			for index_2, one_value in enumerate(l1d):
				sheet_obj.Cell(position[index_2][0], position[index_2][1]).Value = l1d[index_2]

	def make_range_obj(self, sheet_name, xyxy):
		"""
		range객체를 만들기 위한것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.make_range_obj(sheet_name="", xyxy="")
			<object_name>.make_range_obj("sht1", [1,1,3,20])
			<object_name>.make_range_obj("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		return range_obj.Address

	def make_unique_id(self, xyxy, start_no):
		"""
		자리수에 맞는 고유한번호 만들기 (_로 그냥 만들자)
		연속된 같은값일때만, 같은 숫자를 쓴다
		다른곳에 부분적으로 같은 이름이 있을수있다

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param start_no: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.make_unique_id(xyxy="", start_no=100)
			<object_name>.make_unique_id([1,1,3,20], start_no=100)
			<object_name>.make_unique_id([1,1,1,20], start_no=100)
		"""
		l2d = self.read_value_for_range("", xyxy)
		result = []
		x_line_no = len(l2d)
		y_line_no = len(l2d[0])
		change_start_no = start_no

		for y in range(y_line_no):
			new_no = []
			for x in range(x_line_no):
				# 값이 없으면, None값으로 넣는다
				if l2d[x][y] == "" or l2d[x][y] == None:
					new_no.append("")
				else:
					if x == 0:
						new_no = [change_start_no, ]
					else:
						if l2d[x][y] == l2d[x - 1][y]:
							new_no.append(change_start_no)
						else:
							change_start_no = change_start_no + 1
							new_no.append(change_start_no)
			result.append(new_no)
			change_start_no = start_no  # 이부분을 없애면, 고유한 번호들이 할당된다

		for no, l1d in enumerate(result):
			id1 = ""
			for one in l1d:
				id1 = id1 + str(one) + "_"
			result[no].append(id1[:-1])

		return result

	def make_xy_list_for_box_style(self, xyxy):
		"""
		좌표를 주면, 맨끝만 나터내는 좌표를 얻는다

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.make_xy_list_for_box_style(xyxy="")
			<object_name>.make_xy_list_for_box_style([1,1,3,20])
		"""
		temp_1 = []
		for x in [xyxy[0], xyxy[2]]:
			temp = [[x, y] for y in range(xyxy[1], xyxy[3] + 1)]
			temp_1.append(temp)

		temp_2 = []
		for y in [xyxy[1], xyxy[3]]:
			temp = [[x, y] for y in range(xyxy[0], xyxy[2] + 1)]
			temp_2.append(temp)

		result = [temp_1[0], temp_2[1], temp_1[1], temp_2[0]]
		return result

	def merge(self):
		self.range_obj.Merge(0)

	def merge_each_xline(self):
		self.xlapp.DisplayAlerts = False

		for no in range(self.x1, self.x2 + 1):
			l2d = self.read_value_for_range("", [no, self.y1, no, self.y2])
			for one_value in l2d[0]:
				if one_value:
					temp_text = temp_text + str(one_value) + " "
			self.set_range([no, self.y1, no, self.y2])
			self.merge()
			self.sheet_obj.Cells(no, self.y1).Value = temp_text

		self.xlapp.DisplayAlerts = True

	def merge_extend_for_xline(self):
		"""
		선택영역의 각 x라인을 병합하는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.merge_extend_for_xline()
		"""
		x1, y1, x2, y2 = self.get_address_for_selection()
		for x in range(x1, x2 + 1):
			self.merge_for_range("", [x, y1, x, y2])

	def merge_for_range(self, sheet_name, xyxy):
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Merge(0)

	def merge_left_2_ylines(self):
		if self.x1 == self.x2:
			pass
		else:
			for x in range(self.x1, self.x2 + 1):
				self.sheet_obj.Range(self.sheet_obj.Cells(x, self.y1), self.sheet_obj.Cells(x, self.y1 + 1)).Merge(0)

	def merge_left_2_ylines_for_range(self, sheet_name, xyxy):
		"""
		선택 영역중 바로 위의것과 아랫것만 병합하는것
		왼쪽의 2줄을 병합하는 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.merge_left_2_ylines_for_range(sheet_name="", xyxy="")
			<object_name>.merge_left_2_ylines_for_range("sht1", [1,1,3,20])
			<object_name>.merge_left_2_ylines_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		if x1 == x2:
			pass
		else:
			for x in range(x1, x2 + 1):
				sheet_obj.Range(sheet_obj.Cells(x, y1), sheet_obj.Cells(x, y1 + 1)).Merge(0)

	def merge_range(self, sheet_name, xyxy):
		"""
		셀들을 병합하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.merge_range(sheet_name="", xyxy="")
			<object_name>.merge_range("sht1", [1,1,3,20])
			<object_name>.merge_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Merge(0)

	def merge_selection(self):
		"""
		셀들을 병합하는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.merge_selection()
		"""
		range_obj = self.xlapp.Selection
		range_obj.Merge(0)

	def merge_top_2_xlines(self):
		if self.y1 == self.y2:
			pass
		else:
			for y in range(self.y1, self.y2 + 1):
				self.sheet_obj.Range(self.sheet_obj.Cells(self.x1, y), self.sheet_obj.Cells(self.x1 + 1, y)).Merge(0)

	def merge_top_2_xlines_for_range(self, sheet_name, xyxy):
		"""
		선택 영역중 바로 위의것과 아랫것만 병합하는것
		제일위의 2줄만 세로씩 병합하는 것이다
		가로줄 갯수만큰 병합하는것
		위와 아래에 값이 있으면 알람이 뜰것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.merge_top_2_xlines_for_range(sheet_name="", xyxy="")
			<object_name>.merge_top_2_xlines_for_range("sht1", [1,1,3,20])
			<object_name>.merge_top_2_xlines_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		if y1 == y2:
			pass
		else:
			for y in range(y1, y2 + 1):
				sheet_obj.Range(sheet_obj.Cells(x1, y), sheet_obj.Cells(x1 + 1, y)).Merge(0)

	def merge_with_same_uppercell_for_range(self, sheet_name, xyxy):
		"""
		값이 같으면 병합을 시키는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.merge_with_same_uppercell(sheet_name="", xyxy="")
			<object_name>.merge_with_same_uppercell("sht1", [1,1,3,20])
			<object_name>.merge_with_same_uppercell("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		self.xlapp.DisplayAlerts = False
		for y in range(y1, y2 + 1):
			old_value = False
			same_no = 0
			for x in range(x1, x2 + 1):
				one_value = ""
				sheet_obj.Cells(x, y).Value
				if old_value == one_value:
					same_no = same_no + 1
					self.delete_value_for_cell(sheet_name, [x, y])
				else:
					if same_no >= 1:
						self.merge_range(sheet_name, [x - same_no - 1, y, x - 1, y])
						old_value = one_value
						same_no = 0

	def merge_xline_for_range_by_each_xline(self, sheet_name, xyxy):
		"""
		가끔은 여러줄의 x라인을 각각 병합을 하고싶은때가 있다.
		그럴때 사용하기위한 목적이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.merge_xline_for_range_by_each_xline(sheet_name="", xyxy="")
			<object_name>.merge_xline_for_range_by_each_xline("sht1", [1,1,3,20])
			<object_name>.merge_xline_for_range_by_each_xline("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		self.xlapp.DisplayAlerts = False

		for no in range(x1, x2 + 1):
			l2d = self.read_value_for_range("", [no, y1, no, y2])
			for one_value in l2d[0]:
				if one_value:
					temp_text = temp_text + str(one_value) + " "
			self.merge_range(sheet_name, [no, y1, no, y2])
			sheet_obj.Cells(no, y1).Value = temp_text

		self.xlapp.DisplayAlerts = True

	def merge_xyxy(self, sheet_name, xyxy):
		"""
		merge_for_range를 참조하세요

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.merge_xyxy(sheet_name="", xyxy="")
			<object_name>.merge_xyxy("sht1", [1,1,3,20])
			<object_name>.merge_xyxy("", "")
		"""
		self.merge_for_range(sheet_name, xyxy)

	def messagebox(self, input_value):
		win32gui.MessageBox(0, input_value, input_value, 0)

	def move_activecell_to_bottom_for_range(self, sheet_name, xyxy):
		"""
		선택한 위치에서 제일왼쪽, 제일아래로 이동
		xlDown: - 4121,xlToLeft : - 4159, xlToRight: - 4161, xlUp : - 4162

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_activecell_to_bottom_for_range(sheet_name="", xyxy="")
			<object_name>.move_activecell_to_bottom_for_range("sht1", [1,1,3,20])
			<object_name>.move_activecell_to_bottom_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.End(-4121).Select()

	def move_cell(self, sheet1, xy_from, sheet2, xy_to):
		"""
		1 개의 셀만 이동시키는 것. 다른 시트로 이동도 가능

		:param sheet1: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy_from: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param sheet2: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy_to: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_cell(sheet1="", xy_from="", sheet2="", xy_to=[1,1,5,12])
			<object_name>.move_cell("sht1", "", "", [1,1,5,12], "yel70")
			<object_name>.move_cell(sheet1="sht2", xy_from=[1,1,3,5], sheet2="", xy_to=[2,2,5,12])
		"""

		sheet_obj_1 = self.check_sheet_name(sheet1)
		sheet_obj_2 = self.check_sheet_name(sheet2)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xy_from)
		sheet_obj_1.Cells(x1, y1).Cut()
		self.change_any_address_to_xyxy(xy_to)
		range_obj = sheet_obj_2.Cells(x1, y1)
		sheet_obj_2.Paste(range_obj)

	def move_cell_value_to_another_sheet(self, sheet_list, xy_list):
		"""
		다른시트로 값1개 옮기기

		:param sheet_list: (list) [시트이름1, 시트이름2], [[2,3]. [4,5]]
		:param xy_list: (list) 리스트형식의 셀의 주소가 들어가있는 2차원 리스트형식의 자료, [[1, 1], [2, 3], [2, 4]]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_cell_value_to_another_sheet(sheet_list=["sht1", "sht2"], xy_list=[[1, 1], [2, 2]])
			<object_name>.move_cell_value_to_another_sheet(["sht1", "sht2"], [[1, 1], [2, 2]])
			<object_name>.move_cell_value_to_another_sheet(sheet_list=["sht21", "sht2"], xy_list=[[1, 1], [2, 2]])
		"""

		sheet_list = self.check_input_data(sheet_list)
		xy_list = self.check_input_data(xy_list)

		sheet_obj_1 = self.check_sheet_name(sheet_list[0])
		x1, y1 = xy_list[0]
		sheet_obj_1.Cells(x1, y1).Cut()

		sheet_obj_2 = self.check_sheet_name(sheet_list[1])
		x2, y2 = xy_list[1]
		sheet_obj_2.Cells(x2, y2).Insert()

	def move_each_xline_data_as_like_label_print_style_at_new_sheet(self, xyxy, repeat_no, start_xy):
		"""
		x라인의 가로 한줄의 자료를 여반복갯수에 따라서 시작점에서부터 아래로 복사하는것
		입력자료 : 1줄의 영역, 반복하는 갯수, 자료가 옮겨갈 시작주소

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param repeat_no: (int) 반복횟수를 나타내는 정수형 숫자
		:param start_xy: (list or str) 셀영역으로 [1,2], ''(현재 선택 영역)로 사용가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_each_xline_data_as_like_label_print_style_at_new_sheet(xyxy="", repeat_no=2, start_xy=[1,1])
			<object_name>.move_each_xline_data_as_like_label_print_style_at_new_sheet("", 2, [1,1])
			<object_name>.move_each_xline_data_as_like_label_print_style_at_new_sheet(xyxy=[1,1,4,7], repeat_no=2, start_xy=[1,1])
		"""
		sheet_obj = self.check_sheet_name("")
		all_data_set = self.read_value_for_range("", xyxy)
		for no in range(len(all_data_set[0])):
			mok, namuji = divmod(no, repeat_no)
			new_x = mok + start_xy[0]
			new_y = namuji + start_xy[1]
			sheet_obj.Cells(new_x, new_y).Value = all_data_set[0][no]

	def move_each_yline_data_as_like_label_print_style_at_new_sheet(self, xyxy, repeat_no, start_xy):
		"""
		y라인의 가로 한줄의 자료를 여반복갯수에 따라서 시작점에서부터 아래로 복사하는것

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param repeat_no: (int) 반복횟수를 나타내는 정수형 숫자
		:param start_xy: (list or str) 셀영역으로 [1,2], ''(현재 선택 영역)로 사용가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_each_yline_data_as_like_label_print_style_at_new_sheet(xyxy="", repeat_no=2, start_xy=[1,1])
			<object_name>.move_each_yline_data_as_like_label_print_style_at_new_sheet("", 2, [1,1])
			<object_name>.move_each_yline_data_as_like_label_print_style_at_new_sheet(xyxy=[1,1,4,7], repeat_no=2, start_xy=[1,1])
		"""
		sheet_obj = self.check_sheet_name("")
		all_data_set = self.read_value_for_range("", xyxy)
		for no in range(len(all_data_set)):
			mok, namuji = divmod(no, repeat_no)
			new_x = mok + start_xy[0]
			new_y = namuji + start_xy[1]
			sheet_obj.Cells(new_x, new_y).Value = all_data_set[no][0]

	def move_line_obj(self, line_obj):
		"""
		선객체를 다른곳으로 옮기는 것

		:param line_obj: (object) 객체, 라인객체
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_line_obj(line_obj=obj1)
			<object_name>.move_line_obj(obj1)
			<object_name>.move_line_obj(line_obj=obj123)
		"""
		line_obj.Select()
		# self.selection.ShapeRange.ScaleWidth(Factor, RelativeToOriginalSize, Scale)
		self.xlapp.Selection.ShapeRange.ScaleWidth(1, 0, 0)
		self.xlapp.Selection.ShapeRange.ScaleHeight(-1.3, 0, 0)

	def move_line_obj_for_width_n_height(self, line_obj, width_float=12.3, height_float=8.8):
		"""
		선객체의 넓이와 높이를 바꾸는 것

		:param line_obj: (object) 객체, 라인객체
		:param width_float: (int) 넓이를 나타내는 정수
		:param height_float: (int) 높이를 나타내는 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_line_obj_for_width_n_height(line_obj="object1", width_float=12.3, height_float=8.8)
			<object_name>.move_line_obj_for_width_n_height("object1", 12.3, 8.8)
			<object_name>.move_line_obj_for_width_n_height(line_obj="object7", width_float=10.3, height_float=8.8)
		"""
		line_obj.ShapeRange.ScaleWidth = width_float
		line_obj.ShapeRange.ScaleHeight = height_float

	def move_position_in_selection(self, sheet_name, xyxy, insert_step=2, insert_no=1, range_ext=False, del_or_ins="ins"):
		"""
		선택영역의 가로열을 몇개씩 추가하거나 삭제하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param insert_step: (int) 몇번째마다, 삽입이나 삭제를 할것인지
		:param insert_no:  (int) 몇개씩 넣을것인지
		:param range_ext: (bool) 넘어가는 자료가 있으면, 영역을 넘어서 글씨를 쓸것인지 아닌지를 설정
		:param del_or_ins: (str) 삭제인지 아니면 추가인지를 확인하는것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_position_in_selection(sheet_name="", xyxy="", insert_step=2, insert_no=1, range_ext=False, del_or_ins="ins")
			<object_name>.move_position_in_selection("", "", 2, 1, False, "ins")
			<object_name>.move_position_in_selection(sheet_name="sht1", xyxy="", insert_step=2, insert_no=1, range_ext=False, del_or_ins="ins")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		data_2d = self.read_value_for_range(sheet_name, xyxy)
		changed_data_2d = []
		for l1d in data_2d:
			temp = [one for one in l1d]
			changed_data_2d.append(temp)

		empty_1d = ["" for _ in changed_data_2d[0]]
		actual_position = 0

		if del_or_ins == "ins":
			for no in range(len(changed_data_2d)):
				mok = (no + 1) % insert_step
				if mok == 0:
					for no_1 in range(insert_no):
						changed_data_2d.insert(actual_position, empty_1d)
						actual_position = actual_position + 1
				actual_position = actual_position + 1
		self.write_range(sheet_name, xyxy, changed_data_2d)

	def move_range_for_sheet(self, sheet_name1, xyxy1, sheet_name2, xyxy2):
		"""
		모든값을 그대로 이동시키는 것
		cut -> paste

		:param sheet_name1: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy1: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호]), 옮기기 전의 영역
		:param sheet_name2: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy2: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호]), 옮길 후의 영역
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_range(sheet_name1="", xyxy1="", sheet_name2="", xyxy2=[1,1,5,12])
			<object_name>.move_range("sht1", "", "", [1,1,5,12])
			<object_name>.move_range(sheet_name1="sht2", xyxy1=[1,1,3,5], sheet_name2="", xyxy2=[2,2,5,12])
		"""

		sheet_obj_old = self.check_sheet_name(sheet_name1)
		sheet_obj_new = self.check_sheet_name(sheet_name2)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy1)
		range_obj1 = sheet_obj_old.Range(sheet_obj_old.Cells(x1, y1), sheet_obj_old.Cells(x2, y2))
		range_obj1.Cut()
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy2)
		range_obj2 = sheet_obj_new.Range(sheet_obj_new.Cells(x1, y1), sheet_obj_new.Cells(x2, y2))
		sheet_obj_new.Paste(range_obj2)

	def move_range_ystep(self, sheet_name, xyxy, input_yno, step_no):
		"""
		가로의 자료를 설정한 갯수만큼 한줄로 오른쪽으로 이동

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_y: (int) 1부터 시작하는 세로를 나타내는 column의 숫자
		:param step_no:(int) 번호, 반복되는 횟수의 번호, step의 의미 : 간격을 두고 값을 쓸때 (예 : 현재 위치를 기준으로 가로로 2칸씩, 세로로 3칸씩 반복되는 위치에 쓸때)
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_range_ystep(sheet_name="", xyxy="", input_yno=3, step_no=1 )
			<object_name>.move_range_ystep(sheet_name="sht1", xyxy=[1,1,4,7], input_yno=5, step_no=3 )
			<object_name>.move_range_ystep(sheet_name="", xyxy="", input_yno=7, step_no=2)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		new_x = 0
		new_y = input_yno
		for x in range(xyxy[0], xyxy[2] + 1):
			for y in range(xyxy[1], xyxy[3] + 1):
				new_x = new_x + 1
				value = sheet_obj.Cells(x, y).Value
				if value == None:
					value = ""
				sheet_obj.Cells(new_x, new_y).Value = value

	def move_rangevalue_line_value(self, sheet_name, xyxy):
		"""
		선택한영역의 자료를 세로의 한줄로 만드는것
		새로운 세로행을 만든후 그곳에 두열을 서로 하나씩 포개어서 값넣기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_rangevalue_line_value(sheet_name="", xyxy="")
			<object_name>.move_rangevalue_line_value("sht1", [1,1,3,20])
			<object_name>.move_rangevalue_line_value("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		output_list = self.read_value_for_range(sheet_name, xyxy)
		make_one_list = self.yt.list_change_2d_1d(output_list)
		self.insert_yy(sheet_name, y2 + 1)
		self.write_range_value_ydirection_only(sheet_name, [x1, y2 + 1], make_one_list)

	def move_selection_to_bottom(self, sheet_name, xyxy):
		"""
		선택한 위치에서 제일왼쪽, 제일아래로 이동
		xlDown: - 4121,xlToLeft : - 4159, xlToRight: - 4161, xlUp : - 4162

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_activecell_to_bottom(sheet_name="", xyxy="")
			<object_name>.move_activecell_to_bottom("sht1", [1,1,3,20])
			<object_name>.move_activecell_to_bottom("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.End(-4121).Select()

	def move_shape(self, sheet_name, input_shape_obj, top=20, left=30):
		"""
		도형 이동하기

		:param input_shape_obj: 이동시림 도형 이름
		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_shape_obj: (object) 객체, 도형 객체
		:param top: (int) 위쪽을 나타내는 셀번호, row의 숫자 번호
		:param left: (int) 왼쪽을 나타내는 셀번호, column의 숫자 번호
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_shape(sheet_name="", input_shape_obj="object1", top=20, left=30)
			<object_name>.move_shape("", "object1", 20, 30)
			<object_name>.move_shape(sheet_name="sht1", input_shape_obj="object12", top=20, left=30)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		shape_obj = sheet_obj.Shapes(input_shape_obj)
		shape_obj.Top = shape_obj.Top + top
		shape_obj.Left = shape_obj.Left + left

	def move_shape_by_xywh(self, input_shape_obj, input_xywh):
		"""
		도형을 이동시키는 것
		현재위치에서 input_xywh (왼쪽위, 왼쪽, 넓이, 높이)픽셀 값을 기준으로 만드는 것 :

		:param input_shape_obj: (object) 객체,
		:param input_xywh: (list or str) 입력으로 들어오는 주소값으로 형태이며, 문자열의 형태나 리스트형태가 가능하다. 보통 [1,1,2,2]의형태이며, ""을 입력한 경우는 주소를 계산하는 부분에서 현재 선택영역을 기준으로 리스트형태로 만든다
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_shape_by_xywh(input_shape_obj="object1", input_xywh=[3,3,20,30])
			<object_name>.move_shape_by_xywh("object1", [3,3,20,30])
			<object_name>.move_shape_by_xywh(input_shape_obj="object2", input_xywh=[3,3,20,30])
		"""
		input_shape_obj.Top = input_xywh[0]
		input_shape_obj.Left = input_xywh[1]
		input_shape_obj.Width = input_xywh[2]
		input_shape_obj.Height = input_xywh[3]

	def move_shape_position(self, sheet_name, shape_no=3, top=10, left=30):
		"""
		도형을 이동 시키는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param shape_no: (int) 정수, 이동시킬 도형 이름
		:param top: (int) 위쪽을 나타내는 셀번호, row의 숫자 번호
		:param left: (int) 왼쪽을 나타내는 셀번호, column의 숫자 번호
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_shape_position(sheet_name="", shape_no=3, top=10, left=30)
			<object_name>.move_shape_position("", 3, 10, 30)
			<object_name>.move_shape_position(sheet_name="sht1", shape_no=3, top=10, left=30)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.Shapes(shape_no).Top = top
		sheet_obj.Shapes(shape_no).Left = left

	def move_shape_position_by_dxy(self, sheet_name, shape_no, dxy):
		"""
		도형을 이동시키는 것
		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param shape_no: (int) 정수 이동시킬 도형 이름
		:param dxy: (list) 현재의 위치에서 각도를 옮기는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_shape_position_by_dxy(sheet_name="", shape_no=3, dxy=[20,30])
			<object_name>.move_shape_position_by_dxy("sht1", 13, [20,30])
			<object_name>.move_shape_position_by_dxy(sheet_name="sht3", shape_no=3, dxy=[20,30])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		shape_no = self.check_shape_name(sheet_name, shape_no)
		sheet_obj.Shapes(shape_no).IncrementLeft(dxy[1])
		sheet_obj.Shapes(shape_no).IncrementTop(dxy[0])

	def move_sheet_position_by_no(self, sheet_name, input_no):
		"""
		선택된 시트를 앞에서 몇번째로 이동시키는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_index: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_sheet_position_by_no(sheet_name="", input_no=7)
			<object_name>.move_sheet_position_by_no("", 7)
			<object_name>.move_sheet_position_by_no(sheet_name="sht1", input_no=7)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)

		all_shhet_names = self.get_sheet_names()
		current_sheet_no = 0
		for index, value in enumerate(all_shhet_names):
			if sheet_name == value:
				current_sheet_no = index + 1
				break

		if input_no <= current_sheet_no:
			move_to = input_no
		else:
			move_to = input_no + 1

		sheet_obj.Move(Before=self.xlbook.Worksheets(move_to))

	def move_sheet_to_end(self, sheet_name):
		"""
		시트를 제일 앞으로 이동시키는 방법
		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_sheet_to_end(sheet_name="")
			<object_name>.move_sheet_to_end("sht1")
			<object_name>.move_sheet_to_end("")
		"""
		self.xlbook.Worksheets(sheet_name).Move(None, After=self.xlbook.Worksheets(self.xlbook.Worksheets.Count))

	def move_sheet_with_new_file(self, sheet_name):
		"""
		시트를 제일 앞으로 이동시키는 방법

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_sheet_with_new_file(sheet_name="")
			<object_name>.move_sheet_with_new_file("sht1")
			<object_name>.move_sheet_with_new_file("")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.Move(After=self.xlbook.Worksheets(1))

	def move_sheets_to_another_workbook(self, son_xl, mother_xl):
		"""
		모든 엑셀시트를 다른곳으로 이동
		엑셀 애플리케이션 시작

		:param son_xl: (str) 엑셀의 화일이름
		:param mother_xl: (str) 엑셀의 화일이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_sheets_to_another_workbook(son_xl="file1.xlsx", mother_xl="file2.xlsx")
			<object_name>.move_sheets_to_another_workbook("file1.xlsx", "file2.xlsx")
			<object_name>.move_sheets_to_another_workbook(son_xl="fileold1.xlsx", mother_xl="file2.xlsx")
		"""
		sheets_name = son_xl.get_sheet_names()
		for sheet_name1 in sheets_name:
			sheet_obj = son_xl.check_sheet_name(sheet_name1)
			sheet_obj.Copy(Before=mother_xl.xlbook.Worksheets[1])

	def move_value_for_range_to_left_except_emptycell(self, sheet_name, xyxy):
		"""
		x열을 기준으로 값이 없는것은 왼쪽으로 옮기기
		전체영역의 값을 읽어오고, 하나씩 다시 쓴다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_value_for_range_to_left_except_emptycell(sheet_name="", xyxy="")
			<object_name>.move_value_for_range_to_left_except_emptycell("sht1", [1,1,3,20])
			<object_name>.move_value_for_range_to_left_except_emptycell("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		l2d = self.read_value_for_range(sheet_name, xyxy)

		self.delete_value_for_range(sheet_name, xyxy)
		for x in range(0, x2 - x1 + 1):
			new_y = 0
			for y in range(0, y2 - y1 + 1):
				value = l2d[x][y]
				if value == "" or value == None:
					pass
				else:
					sheet_obj.Cells(x + x1, new_y + y1).Value = value
					new_y = new_y + 1

	def move_value_if_startwith_input_value_after_insert_new_line(self, sheet_name, xyxy, startwith="*"):
		"""
		맨앞부분에 세로줄을 하나 만든후
		입력값으로받은 글자와 각 셀의 앞부분부터 같은 값일경우 한줄 앞으로 값을 이동시키는 것

		가끔 많은 자료를 구분하는 경우가 필요해서 만든 것이다
		맨앞에 특정글자가 있으면, 앞으로 옮기기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param startwith: (str) 문자의 시작을 나타내는 형태
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_value_if_startwith_input_value_after_insert_new_line(sheet_name="", xyxy="", startwith="*")
			<object_name>.move_value_if_startwith_input_value_after_insert_new_line("", [1,1,3,20],startwith="*")
			<object_name>.move_value_if_startwith_input_value_after_insert_new_line("sht1", [1,1,1,20],startwith="*")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x, y, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		self.insert_yline("", y)
		for one_x in range(x, x2):
			one_value = self.read_value_for_cell("", [one_x, y + 1])
			if one_value.startswith(startwith):
				sheet_obj.Cells(one_x, y).Value = one_value
				sheet_obj.Cells(one_x, y + 1).Value = None

	def move_value_of_range_to_another_sheet(self, sheet_name1, xyxy1, sheet_name2, xyxy2):
		"""
		모든값을 그대로 이동시키는 것
		cut -> paste

		:param sheet_name1: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy1: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param sheet_name2: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy2: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_xxline_to_another_sheet(sheet_name1="sht1",  xyxy1=[1, 3, 5], sheet_name2="sht2",xyxy2=[8,10,20])
			<object_name>.move_xxline_to_another_sheet("sht1", [1, 3, 5], "sht2", [8,10,20])
			<object_name>.move_xxline_to_another_sheet(sheet_name1="sht11", xyxy1=[1, 3, 5], sheet_name2="sht12", xyxy2=[8,10,20])
		"""
		sheet_obj_old = self.check_sheet_name(sheet_name1)
		sheet_obj_new = self.check_sheet_name(sheet_name2)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy1)
		range_obj1 = sheet_obj_old.Range(sheet_obj_old.Cells(x1, y1),
											  sheet_obj_old.Cells(x2, y2))
		range_obj1.Cut()
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy2)
		range_obj2 = sheet_obj_new.Range(sheet_obj_new.Cells(x1, y1),
										 sheet_obj_new.Cells(x2, y2))
		sheet_obj_new.Paste(range_obj2)

	def move_value_to_another_sheet(self, sheet_name1, xyxy1, sheet_name2, xyxy2):
		sheet_obj_old = self.check_sheet_name(sheet_name1)
		sheet_obj_new = self.check_sheet_name(sheet_name2)
		[self.x1, self.y1, self.x2, self.y2] = self.change_any_address_to_xyxy(xyxy1)
		range_obj1 = sheet_obj_old.Range(sheet_obj_old.Cells(self.x1, self.y1),
										 sheet_obj_old.Cells(self.x2, self.y2))
		range_obj1.Cut()
		[self.x1, self.y1, self.x2, self.y2] = self.change_any_address_to_xyxy(xyxy2)
		range_obj2 = sheet_obj_new.Range(sheet_obj_new.Cells(self.x1, self.y1),
										 sheet_obj_new.Cells(self.x2, self.y2))
		sheet_obj_new.Paste(range_obj2)

	def move_value_to_left_except_emptycell_for_range(self, sheet_name, xyxy):
		"""
		x열을 기준으로 값이 없는것은 왼쪽으로 옮기기
		전체영역의 값을 읽어오고, 하나씩 다시 쓴다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_value_to_left_except_emptycell(sheet_name="", xyxy="")
			<object_name>.move_value_to_left_except_emptycell("sht1", [1,1,3,20])
			<object_name>.move_value_to_left_except_emptycell("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		l2d = self.read_value_for_range(sheet_name, xyxy)
		self.delete_value_for_range(sheet_name, xyxy)
		for x in range(0, x2 - x1 + 1):
			new_y = 0
			for y in range(0, y2 - y1 + 1):
				value = l2d[x][y]
				if value == "" or value == None:
					pass
				else:
					sheet_obj.Cells(x + x1, new_y + y1).Value = value
					new_y = new_y + 1

	def move_xxline_to_another_sheet(self, sheet_name1, sheet_name2, xx_list0, xx_list1):
		"""
		세로의 값을 이동시킵니다

		:param sheet_name1: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param sheet_name2: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xx_list0: (list) 가로만의 영역을 나타내는 2개의 가로줄 번호
		:param xx_list1: (list) 가로만의 영역을 나타내는 2개의 가로줄 번호
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_xxline_to_another_sheet(sheet1="sht1", sheet2="sht2", xx_list0=[1, 3, 5], xx_list1=[8,10,20])
			<object_name>.move_xxline_to_another_sheet("sht1", "sht2", [1, 3, 5], [8,10,20])
			<object_name>.move_xxline_to_another_sheet(sheet1="sht11", sheet2="sht12", xx_list0=[1, 3, 5], xx_list1=[8,10,20])
		"""
		sheet1 = self.check_sheet_name(sheet_name1)
		sheet2 = self.check_sheet_name(sheet_name2)
		xx_list0_1, xx_list0_2 = self.check_xy_address(xx_list0)
		xx_list1_1, xx_list1_2 = self.check_xy_address(xx_list1)
		xx_list0_1 = self.change_char_to_num(xx_list0_1)
		xx_list0_2 = self.change_char_to_num(xx_list0_2)
		xx_list1_1 = self.change_char_to_num(xx_list1_1)
		xx_list1_2 = self.change_char_to_num(xx_list1_2)
		sheet1.Select()
		sheet1.Rows(str(xx_list0_1) + ':' + str(xx_list0_2)).Select()
		sheet1.Rows(str(xx_list0_1) + ':' + str(xx_list0_2)).Copy()
		sheet2.Select()
		sheet2.Rows(str(xx_list1_1) + ':' + str(xx_list1_2)).Select()
		sheet2.Paste()

	def move_yline_for_range(self, sheet_name_list, yy_list):
		"""
		가로의 값을 이동시킵니다

		:param sheet_name_list: (list) 시트의 리름들이 들어있는 1차원의 리스트
		:param yy_list: (list) 세로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_y(sheet_name="", yy_list=[2, 4])
			<object_name>.move_y("", [2, 4])
			<object_name>.move_y("sht1", [3,7])
		"""

		sheet_obj1 = self.check_sheet_name(sheet_name_list[0])
		char_y1 = self.change_num_to_char(yy_list[0])
		range_obj1 = sheet_obj1.Columns(char_y1 + ':' + char_y1)

		sheet_obj2 = self.check_sheet_name(sheet_name_list[1])
		char_y2 = self.change_num_to_char(yy_list[1])
		range_obj2 = sheet_obj2.Columns(char_y2 + ':' + char_y2)

		range_obj1.Select()
		range_obj1.Cut()
		range_obj2.Select()
		range_obj2.Insert()

	def move_yline_value_to_multi_input_lines_for_range(self, xyxy, repeat_no, start_xy):
		"""
		y라인의 가로 한줄의 자료를 여반복갯수에 따라서 시작점에서부터 아래로 복사하는것
		입력자료 : 1줄의 영역, 반복하는 갯수, 자료가 옮겨갈 시작주소

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param repeat_no: (int) 반복횟수를 나타내는 정수형 숫자
		:param start_xy: (list or str) 셀영역으로 [1,2], ''(현재 선택 영역)로 사용가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_yline_value_to_multi_input_lines(xyxy="", repeat_no=2, start_xy=[1,1])
			<object_name>.move_yline_value_to_multi_input_lines("", 2, [1,1])
			<object_name>.move_yline_value_to_multi_input_lines(xyxy=[1,1,4,5], repeat_no=7, start_xy=[1,1])
		"""
		sheet_obj = self.check_sheet_name("")
		all_data_set = self.read_value_for_range("", xyxy)
		for no in range(len(all_data_set)):
			mok, namuji = divmod(no, repeat_no)
			new_x = mok + start_xy[0]
			new_y = namuji + start_xy[1]
			sheet_obj.Cells(new_x, new_y).Value = all_data_set[no][0]

	def move_ystep(self, sheet_name, xyxy, input_xno, step_no):
		"""
		move_ystep(sheet_name="", xyxy="", input_w, step_no)
		가로의 자료를 설정한 갯수만큼 한줄로 오른쪽으로 이동

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_xno: (int) 정수, x를 나타내는 가로줄의 번호, row의 숫자번호
		:param step_no: (int) 정수, n번째마다 반복되는것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_ystep(sheet_name="", xyxy="", input_xno=3, step_no=1 )
			<object_name>.move_ystep(sheet_name="sht1", xyxy=[1,1,4,7], input_xno=5, step_no=3 )
			<object_name>.move_ystep(sheet_name="", xyxy="", input_xno=7, step_no=2)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		new_y = 0
		new_x = input_xno
		for y in range(xyxy[0], xyxy[2] + 1):
			for x in range(xyxy[1], xyxy[3] + 1):
				new_y = new_y + 1
				value = sheet_obj.Cells(x, y).Value
				if value == None:
					value = ""
				sheet_obj.Cells(new_y, new_x).Value = value

	def move_yy(self, sheet_name1, sheet_name2, yy_list0, yy_list1):
		"""
		세로의 값을 이동시킵니다

		:param sheet_name1: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param sheet_name2: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param yy_list0: (list) 2개의 column을 나타내는 리스트형
		:param yy_list1: (list) 2개의 column을 나타내는 리스트형
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_yy(sheet1="sht1", sheet2="sht2", yy_list1=[1, 3, 5], yy_list2=[8,10,20])
			<object_name>.move_yy("sht1", "sht2", [1, 3, 5], [8,10,20])
			<object_name>.move_yy(sheet1="sht11", sheet2="sht12", yy_list1=[1, 3, 5], yy_list2=[8,10,20])
		"""
		self.move_yyline(sheet_name1, sheet_name2, yy_list0, yy_list1)

	def move_yyline_to_another_sheet(self, sheet_name1, sheet_name2, yy_list0, yy_list1):
		sheet1 = self.check_sheet_name(sheet_name1)
		sheet2 = self.check_sheet_name(sheet_name2)
		yy_list0_1, yy_list0_2 = self.check_xy_address(yy_list0)
		yy_list1_1, yy_list1_2 = self.check_xy_address(yy_list1)
		yy_list0_1 = self.change_num_to_char(yy_list0_1)
		yy_list0_2 = self.change_num_to_char(yy_list0_2)
		yy_list1_1 = self.change_num_to_char(yy_list1_1)
		yy_list1_2 = self.change_num_to_char(yy_list1_2)
		sheet1.Select()
		sheet1.Columns(str(yy_list0_1) + ':' + str(yy_list0_2)).Select()
		sheet1.Columns(str(yy_list0_1) + ':' + str(yy_list0_2)).Cut()
		sheet2.Select()
		sheet2.Columns(str(yy_list1_1) + ':' + str(yy_list1_2)).Select()
		sheet2.Columns(str(yy_list1_1) + ':' + str(yy_list1_2)).Insert()

	def move_yyline_to_another_sheet_for_range(self, sheet_name1, sheet_name2, yy_list0, yy_list1):
		"""
		가로의 값을 복사해서 다른곳으로 이동시키기

		:param sheet1: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param sheet2: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param yy_list1: (list) 2개의 column을 나타내는 리스트형
		:param yy_list2: (list) 2개의 column을 나타내는 리스트형
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.move_yyline_to_another_sheet(sheet1="sht1", sheet2="sht2", yy_list1=[1, 3, 5], yy_list2=[8,10,20])
			<object_name>.move_yyline_to_another_sheet("sht1", "sht2", [1, 3, 5], [8,10,20])
			<object_name>.move_yyline_to_another_sheet(sheet1="sht11", sheet2="sht12", yy_list1=[1, 3, 5], yy_list2=[8,10,20])
		"""
		sheet1 = self.check_sheet_name(sheet_name1)
		sheet2 = self.check_sheet_name(sheet_name2)
		yy_list0_1, yy_list0_2 = self.check_xy_address(yy_list0)
		yy_list1_1, yy_list1_2 = self.check_xy_address(yy_list1)
		yy_list0_1 = self.change_num_to_char(yy_list0_1)
		yy_list0_2 = self.change_num_to_char(yy_list0_2)
		yy_list1_1 = self.change_num_to_char(yy_list1_1)
		yy_list1_2 = self.change_num_to_char(yy_list1_2)
		sheet1.Select()
		sheet1.Columns(str(yy_list0_1) + ':' + str(yy_list0_2)).Select()
		sheet1.Columns(str(yy_list0_1) + ':' + str(yy_list0_2)).Cut()
		sheet2.Select()
		sheet2.Columns(str(yy_list1_1) + ':' + str(yy_list1_2)).Select()
		sheet2.Columns(str(yy_list1_1) + ':' + str(yy_list1_2)).Insert()

	def new_button(self, title=""):
		new_btn = self.sheet_obj.Buttons()
		left_px, top_px, width_px, height_px = self.xyxy2_to_pxywh("", [self.x1, self.y1])
		new_btn.Add(left_px, top_px, width_px, height_px)
		new_btn.Text = title

	def new_button_for_range(self, sheet_name, xyxy, title=""):
		"""
		엑셀의 시트위에 버튼을 만드는것.

		버튼을 만들어서 그 버튼에 매크로를 연결하는 데,익서은 그냥 버튼만 만드는 것이다
		Add(왼쪽의 Pixel, 위쪽 Pixce, 넓이, 높이)

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param title: (str) 버튼위에 나타나는 글씨
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_button(sheet_name="", xyxy="", title="버튼이름")
			<object_name>.new_button("", [1,1,3,20], "버튼이름")
			<object_name>.new_button("sht1", [1,1,1,20], "버튼이름")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		new_btn = sheet_obj.Buttons()
		left_px, top_px, width_px, height_px = self.read_coord_for_cell(sheet_name, xyxy)
		new_btn.Add(left_px, top_px, width_px, height_px)
		new_btn.Text = title

	def new_button_with_macro_code(self, macro_code, title=""):
		new_btn = self.sheet_obj.Buttons()
		self.sheet_obj.Cells(self.x1, self.y1).Select()
		left_px, top_px, width_px, height_px = self.xyxy2_to_pxywh("", [self.x1, self.y1])
		new_btn.Add(left_px, top_px, width_px, height_px)
		new_btn.OnAction = macro_code
		new_btn.Text = title

	def new_button_with_macro_code_for_range(self, sheet_name, xyxy, macro_code="", title=""):
		"""
		매크로랑 연결된 버튼을 만드는것
		버튼을 만들어서 그 버튼에 매크로를 연결하는 것이다
		매크로와 같은것을 특정한 버튼에 연결하여 만드는것을 보여주기위한 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param macro_code: (str) macro code, 매크로 코드
		:param title: (str) caption for button, 버튼위에 나타나는 글씨
		:return: X / 없음
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_button_with_macro(sheet_name="", xyxy="", macro_code="name2", title="입력1")
			<object_name>.new_button_with_macro("", [1,1,3,20], macro_code="name2", title="입력1")
			<object_name>.new_button_with_macro("sht1", [1,1,1,20], macro_code="name2", title="입력1")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		new_btn = sheet_obj.Buttons()
		sheet_obj.Cells(x1, y1).Select()
		left_px, top_px, width_px, height_px = self.read_coord_for_cell("", [x1, y1])
		new_btn.Add(left_px, top_px, width_px, height_px)
		new_btn.OnAction = macro_code
		new_btn.Text = title

	def new_button_with_macro_name(self, macro_name, title=""):
		new_btn = self.sheet_obj.Buttons()
		left_px, top_px, width_px, height_px = self.xyxy2_to_pxywh("", [self.x1, self.y1])
		new_btn.Add(left_px, top_px, width_px, height_px)
		new_btn.OnAction = macro_name
		new_btn.Text = title

	def new_button_with_macro_name_for_range(self, sheet_name, xyxy, macro_name="", title=""):
		"""
		버튼을 만들어서 그 버튼에 입력된 매크로를 연결하는 것이다
		매크로와 같은것을 특정한 버튼에 연결하여 만드는것을 보여주기위한 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param macro_code: (str) 매크로 코드
		:param title: (str) 버튼위에 나타나는 글씨
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_button_with_macro_name(sheet_name="", xyxy="", macro_name="name2", title="입력1")
			<object_name>.new_button_with_macro_name("", [1,1,3,20], macro_name="name2", title="입력1")
			<object_name>.new_button_with_macro_name("sht1", [1,1,1,20], macro_name="name2", title="입력1")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		sheet_obj = self.check_sheet_name(sheet_name)
		new_btn = sheet_obj.Buttons()
		left_px, top_px, width_px, height_px = self.read_coord_for_cell("", xyxy)
		new_btn.Add(left_px, top_px, width_px, height_px)
		new_btn.OnAction = macro_name
		new_btn.Text = title

	def new_cell_obj(self, sheet_name, xy):
		"""
		입력 셀의 객체를 만들어서 돌려준다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_cell_obj(sheet_name="", xy=[7,7])
			<object_name>.get_cell_obj("", [3,20])
			<object_name>.get_cell_obj("", [1,20])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		one_cell = sheet_obj.Cells(xy[0], xy[1])
		return one_cell

	def new_chart(self, chart_type, input_pxywh, source_xyxy):
		chart_obj = self.sheet_obj.Chartobjects.Add(input_pxywh)
		[self.x1, self.y1, self.x2, self.y2] = self.change_any_address_to_xyxy(source_xyxy)
		r1c1 = self.xyxy2_to_r1c1([self.x1, self.y1, self.x2, self.y2])
		range_obj = self.sheet_obj.Range(r1c1)
		chart_obj.SetSourceData(range_obj)
		chart_obj.ChartType = chart_type
		return chart_obj

	def new_chart_for_range(self, sheet_name, dispaly_xyxy="", chart_style=1, data_xyxy="", main_title="제목1"):
		"""
		챠트를 만드는 것 기본적인 설정을 해서 만듭니다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param dispaly_xyxy: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param chart_style: (int) 차트의 스타일을 나타내는 번호
		:param data_xyxy: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param main_title: (str) 제목을 나태내기 위한 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_chart(sheet_name="", dispaly_xyxy="", chart_style=1, data_xyxy="", main_title="제목1")
			<object_name>.new_chart("", [1,1,3,20], 1, [10,13,24,35], "title1")
			<object_name>.new_chart("sht1", [1,1,1,20], chart_style=1, data_xyxy="", main_title="제목1")
		"""
		chart_style_vs_enum = {"line": 4, "pie": 5}
		sheet_obj = self.check_sheet_name(sheet_name)
		data_range_obj = sheet_obj.Range(sheet_obj.Cells(data_xyxy[0], data_xyxy[1]),
										 sheet_obj.Cells(data_xyxy[2], data_xyxy[3]))
		pxywh = self.xyxy2_to_pxywh(sheet_name, dispaly_xyxy)
		chart_obj_all = sheet_obj.ChartObjects().Add(pxywh[0], pxywh[1], pxywh[2], pxywh[3])
		chart_obj_all.Chart.SetSourceData(Source=data_range_obj)
		chart_obj = chart_obj_all.Chart
		chart_obj.ChartType = chart_style_vs_enum[chart_style]
		if main_title:
			chart_obj.HasTitle = True  # 차트 제목 나오게(False면 안보임) chart_obj.ChartTitle.Text = main_title # 차트 제목 설정
		return chart_obj

	def new_excel_file_for_range(self, sheet_name, xyxy, input_filename="D:\\aaa.xlsx"):
		"""
		현재화일의 자료를 복사해서
		선택영역에서 같은 영역의 자료들만 묶어서 엑셀화일 만들기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_filename: (str) 화일의 이름을 나타내는 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_excel_file_for_range(sheet_name="", xyxy="", input_filename="D:\\my_file.xlsx")
			<object_name>.new_excel_file_for_range("", "", "D:\\my_file.xlsx")
			<object_name>.new_excel_file_for_range("sht1", "", "D:\\my_file2.xlsx")
		"""

		range_obj = self.make_range_obj(sheet_name, xyxy)
		range_obj.Select()
		self.xlapp.selection.Copy()
		self.new_workbook("")
		sheet_obj = self.check_sheet_name("")
		sheet_obj.Cells(1, 1).Select()
		sheet_obj.Paste()
		self.save(input_filename)

	def new_image(self, file_path, input_xywh, link, image_in_file):
		rng = self.sheet_obj.Cells(input_xywh[0], input_xywh[1])
		# sh.Shapes.AddPicture("화일이름", "링크가있나", "문서에저장", "x좌표", "y좌표", "넓이","높이")
		self.sheet_obj.Shapes.AddPicture(file_path, link, image_in_file, rng.Left, rng.Top, input_xywh[2],
										 input_xywh[3])

	def new_image_by_pixel(self, sheet_name, file_path="D:\\aaa.xlsx", pxywh=[30, 30, 20, 30], link=0, image_in_file=1):
		"""
		그림을 픽셀크기로 시트에 넣는 것
		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param file_path: (str) 입력으로 들어오는 텍스트, 화일의 경로, file_path
		:param pxywh: (list) [영역중 왼쪽위의 x축의 픽셀번호, 영역중 왼쪽위의 y축의 픽셀번호, 넓이를 픽셀로 계산한것, 높이를 픽셀로 계산한것]
		:param link: (str) 링크를 나타내는 문자열
		:param image_in_file: (str) 입력으로 들어오는 텍스트, 화일이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_image_by_pixel(sheet_name="", file_path="D:\\aaa.xlsx", pxywh=[30,30, 20, 30], link=0, image_in_file=1)
			<object_name>.new_image_by_pixel("", "D:\\aaa.xlsx", [30,30, 20, 30], 0, 1)
			<object_name>.new_image_by_pixel(sheet_name="sht1", file_path="D:\\aaa.xlsx", pxywh=[30,30, 40, 30], link=0, image_in_file=1)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.Shapes.AddPicture(file_path, link, image_in_file, pxywh[0], pxywh[1], pxywh[2], pxywh[3])

	def new_image_for_cell(self, sheet_name, xy, input_full_path="D:\\my_folder"):
		"""
		셀 하나에 그림을 맞춰서 넣는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param input_full_path: (str) 입력으로 들어오는 텍스트, 화일의 경로, file_path
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_image_for_cell(sheet_name="", xy="", input_full_path="D:\\my_folder")
			<object_name>.new_image_for_cell(sheet_name="sht1", xy=[4,7], input_full_path="D:\\my_folder1")
			<object_name>.new_image_for_cell(sheet_name="", xy="", input_full_path="D:\\my_folder2")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.Cells(xy[0], xy[1]).Select()
		aaa = sheet_obj.Pictures
		aaa.Insert(input_full_path).Select()

	def new_image_for_range(self, sheet_name, file_path="D:\\aaa.xlsx", input_xywh=[3, 3, 20, 30], link=0, image_in_file=1):
		"""
		image화일을 넣는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param file_path: (str) 입력으로 들어오는 텍스트, 화일의 경로, file_path
		:param input_xywh:  (list or str) 입력으로 들어오는 주소값으로 형태이며, 문자열의 형태나 리스트형태가 가능하다. 보통 [1,1,2,2]의형태이며, ""을 입력한 경우는 주소를 계산하는 부분에서 현재 선택영역을 기준으로 리스트형태로 만든다
		:param link: (str) 링크를 나타내는 문자열
		:param image_in_file: (str) 입력으로 들어오는 텍스트, 화일이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_image(sheet_name="", file_path="D:\\aaa.xlsx", input_xywh=[30,30, 20, 30], link=0, image_in_file=1)
			<object_name>.new_image("", "D:\\aaa.xlsx", [30,30, 20, 30], 0, 1)
			<object_name>.new_image(sheet_name="sht1", file_path="D:\\aaa.xlsx", input_xywh=[30,30, 40, 30], link=0, image_in_file=1)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		rng = sheet_obj.Cells(input_xywh[0], input_xywh[1])
		# sh.Shapes.AddPicture("화일이름", "링크가있나", "문서에저장", "x좌표", "y좌표", "넓이","높이")
		sheet_obj.Shapes.AddPicture(file_path, link, image_in_file, rng.Left, rng.Top, input_xywh[2], input_xywh[3])

	def new_image_for_range_for_sheet(self, sheet_name, xyxy, input_filename="D:\\aaa.xlsx", space=1):
		"""
		특정 사진을 셀안에 맞토록 사이즈 조절하는 것
		sh.Shapes.AddPicture("화일이름", "링크가있나”, "문서에저장", "x좌표", "y좌표", "넓이", "높이")

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_filename: (str) 화일의 이름을 나타내는 문자열
		:param space:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_image_for_cell(sheet_name="", xy="", input_full_path="D:\\my_folder",space=1 )
			<object_name>.new_image_for_cell(sheet_name="sht1", xy=[4,7], input_full_path="D:\\my_folder1",space=1 )
			<object_name>.new_image_for_cell(sheet_name="", xy="", input_full_path="D:\\my_folder2", space=1)
		"""

		xy_1 = self.read_coord_for_cell(sheet_name, [xyxy[0], xyxy[1]])
		xy_2 = self.read_coord_for_cell(sheet_name, [xyxy[2], xyxy[3]])

		x_start = xy_1[0] + space
		y_start = xy_1[1] + space

		width = xy_2[0] + xy_2[2] - xy_1[0] - space * 2
		height = xy_2[1] + xy_2[3] - xy_1[1] - space * 2

		sheet_obj = self.check_sheet_name(sheet_name)
		# sh.Shapes.AddPicture("화일이름", "링크가있나", "문서에저장", "x좌표", "y좌표", "넓이","높이")
		sheet_obj.Shapes.AddPicture(input_filename, 0, 1, x_start, y_start, width, height)

	def new_image_for_range_name(self, folder_path, ext_list):
		ext_list = self.check_input_data(ext_list)

		self.select_sheet()
		all_files = self.util.get_all_filename_in_folder_by_extension_name(folder_path, ext_list)  # 1
		all_files.sort()  # 2

		all_rng_name = self.get_range_names()  # 3
		l2d = []
		for one in all_rng_name:
			bbb = self.change_any_address_to_xyxy(one[2])
			bbb.append(one[1])
			l2d.append(bbb)

		l2d.sort()  # 4

		min_count = min(len(l2d), len(all_files))
		for index in range(min_count):
			one_file = all_files[index]
			# insert_all_image_of_folder_for_sheet(self, folder_name, ext_list, xywh, link=0J, image_in_file=1):
			self.new_images_in_folder("", "D:\\", ["jpg"])  # 5

	def new_image_for_range_name_for_sheet(self, sheet_name, folder_path="D:\\aaa.xlsx", ext_list=["jgp", "png"]):
		"""
		입력으로 들어오는 사진을 이름역역안에 맞춰서 넣는 것이다

		1. 입력된 폴더에서 사진의 화일이름을 갖고온다
		2. 사진자료를 이름기준으로 정렬 시킨다
		3. 엑셀의 시트에서 이름영역을 갖고온다
		4. 이름영역의 주소를 기준으로 정렬을 시킨다
		5. 이름영영역의 갯수를 기준으로 사진자료를 넣는다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param folder_path: (str) 입력으로 들어오는 텍스트, 경로를 나타내는 문자열
		:param ext_list:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_image_for_range_name(sheet_name="", file_path="D:\\aaa.xlsx", ext_list=["jgp", "png"])
			<object_name>.new_image_for_range_name("", "D:\\aaa.xlsx", ["jgp", "png"])
			<object_name>.new_image_for_range_name(sheet_name="sht1", file_path="D:\\aaa.xlsx", ext_list=["jgp", "png"])
		"""
		ext_list = self.check_input_data(ext_list)

		self.select_sheet(sheet_name)
		all_files = self.util.get_all_filename_in_folder_by_extension_name(folder_path, ext_list)  # 1
		all_files.sort()  # 2

		all_rng_name = self.read_range_names()  # 3
		l2d = []
		for one in all_rng_name:
			bbb = self.change_any_address_to_xyxy(one[2])
			bbb.append(one[1])
			l2d.append(bbb)

		l2d.sort()  # 4

		min_count = min(len(l2d), len(all_files))
		for index in range(min_count):
			one_file = all_files[index]
			# insert_all_image_of_folder_for_sheet(self, sheet_name, folder_name, ext_list, xywh, link=0J, image_in_file=1):
			self.insert_all_image_of_folder_for_sheet("", "D:\\", ["jpg"])  # 5

	def new_image_for_sheet(self):
		"""
		시트에 그림을 넣는것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_image_for_sheet()
		"""
		sh = self.xlbook.Worksheets("Sheet1")
		sh.Shapes.AddPicture("c:\\icon_sujun.gif", 0, 1, 541.5, 92.25, 192.75, 180)

	def new_images_for_sheet_for_folder(self, sheet_name, folder_name="D:\\aaa", ext_list=["xls"], input_xywh=[3, 3, 20, 30], link="0J", image_in_file=1):
		"""
		특정폴다안이 모든 사진을 전부 불러오는 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param folder_name: (str) 폴더의 이름
		:param ext_list: (list) 화일의 형태를 나타내는 끝의 형식에 대한 리스트형태
		:param input_xywh:  (list or str) 입력으로 들어오는 주소값으로 형태이며, 문자열의 형태나 리스트형태가 가능하다. 보통 [1,1,2,2]의형태이며, ""을 입력한 경우는 주소를 계산하는 부분에서 현재 선택영역을 기준으로 리스트형태로 만든다
		:param link: (str) 링크를 나타내는 문자열
		:param image_in_file: (str) 입력으로 들어오는 텍스트, 화일이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_images_for_sheet_for_folder(sheet_name="", folder_name="D:\\aaa", ext_list=["xls"], input_xywh=[3,3, 20, 30], link="0J", image_in_file=1)
			<object_name>.new_images_for_sheet_for_folder("", "D:\\aaa", ["xls"], [3,3, 20, 30], "0J", image_in_file=1)
			<object_name>.new_images_for_sheet_for_folder(sheet_name="sht1", folder_name="D:\\abc", ext_list=["xls"], input_xywh=[4,5, 20, 30], link="0J", image_in_file=1)
		"""

		aaa = self.util.get_all_filename_in_folder_by_extension_name(folder_name, ext_list)
		sheet_obj = self.check_sheet_name(sheet_name)
		rng = sheet_obj.Cells(input_xywh[0], input_xywh[1])

		for index, filename in enumerate(aaa):
			input_full_path = folder_name + "/" + filename
			input_full_path = str(input_full_path).replace("/", "\\")

			sheet_obj.Shapes.AddPicture(input_full_path, link, image_in_file, rng.Left + index * 5,
										rng.Top + index * 5,
										input_xywh[2], input_xywh[3])
		return aaa

	def new_images_in_folder(self, folder_name, ext_list, input_xywh, link, image_in_file):
		aaa = self.util.get_all_filename_in_folder_by_extension_name(folder_name, ext_list)
		rng = self.sheet_obj.Cells(input_xywh[0], input_xywh[1])

		for index, filename in enumerate(aaa):
			input_full_path = folder_name + "/" + filename
			input_full_path = str(input_full_path).replace("/", "\\")

			self.sheet_obj.Shapes.AddPicture(input_full_path, link, image_in_file, rng.Left + index * 5,
											 rng.Top + index * 5, input_xywh[2], input_xywh[3])
		return aaa

	def new_line_by_pxyxy(self, sheet_name, pxyxy):
		"""
		4개영역의 픽셀값을 가지고 사각형을 그리는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param pxyxy: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.draw_border_line_by_pxyxy(sheet_name="", xyxy="")
			<object_name>.draw_border_line_by_pxyxy("", [1,1,3,20])
			<object_name>.draw_border_line_by_pxyxy("sht1", [1,1,1,20])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		new_shape_obj = sheet_obj.Shapes.AddLine(pxyxy[0], pxyxy[1], pxyxy[2], pxyxy[3])
		return new_shape_obj

	def new_line_for_range(self, sheet_name, xyxy, input_dic):
		"""
		선을 만들기

		:param input_dic: (dic) 사전형으로 입력되는 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.draw_border_line_for_sheet("", "", input_dic = {"key1":1, "line_1":"red", "input_color":"red", "font_bold":1})
			<object_name>.draw_border_line_for_sheet("", "", {"key1":1, "line_1":"red", "input_color":"red", "font_bold":1})
			<object_name>.draw_border_line_for_sheet("", "", input_dic = {"key1":1, "line_2":"red", "input_color1":"red", "font_bold1":1}])
		"""
		enum_line = {
			"msoArrowheadNone": 1, "msoArrowheadTriangle": 2, "msoArrowheadOpen": 3, "msoArrowheadStealth": 4,
			"msoArrowheadDiamond": 5, "msoArrowheadOval": 6,
			"": 1, "<": 2, ">o": 3, ">>": 4, ">": 2, "<>": 5, "o": 6,
			"basic": 1, "none": 1, "triangle": 2, "open": 3, "stealth": 4, "diamond": 5, "oval": 6,
			"msoArrowheadNarrow": 1, "msoArrowheadWidthMedium": 2, "msoArrowheadWide": 3,
			"msoArrowheadShort": 1, "msoArrowheadLengthMedium": 2, "msoArrowheadLong": 3,
			"short": 1, "narrow": 1, "medium": 2, "long": 3, "wide": 3,
			"-1": 1, "0": 2, "1": 3,
			"dash": 4, "dashdot": 5, "dashdotdot": 6, "rounddot": 3, "longdash": 7, "longdashdot": 8,
			"longdashdotdot": 9,
			"squaredot": 2,
			"-": 4, "-.": 5, "-..": 6, ".": 3, "--": 7, "--.": 8, "--..": 9, "ㅁ": 2,
		}

		base_data = {
			"sheet_name": "",
			"xyxy": [100, 100, 0, 0],
			"color": 10058239,
			"line_style": "-.",
			"thickness": 0.5,
			"transparency": 0,
			"head_style": ">",
			"head_length": "0",
			"head_width": "0",
			"tail_style": ">",
			"tail_length": "0",
			"tail_width": "0",
		}

		# 기본자료에 입력받은값을 update하는것이다
		base_data.update(input_dic)

		sheet = self.check_sheet_name(base_data["sheet_name"])
		set_line = sheet.Shapes.AddLine(base_data["xyxy"][0], base_data["xyxy"][1], base_data["xyxy"][2],
										base_data["xyxy"][3])
		set_line.Select()
		set_line.Line.ForeColor.RGB = base_data["color"]
		set_line.Line.DashStyle = enum_line[base_data["line_style"]]
		set_line.Line.Weight = base_data["thickness"]
		set_line.Line.Transparency = base_data["transparency"]
		# print(set_line.Name)
		# 엑셀에서는 Straight Connector 63의 형태로 이름이 자동적으로 붙여진다

		set_line.Line.BeginArrowheadStyle = enum_line[base_data["head_style"]]
		set_line.Line.BeginArrowheadLength = enum_line[base_data["head_length"]]
		set_line.Line.BeginArrowheadWidth = enum_line[base_data["head_width"]]
		set_line.Line.EndArrowheadStyle = enum_line[base_data["tail_style"]]  # 화살표의 머리의 모양
		set_line.Line.EndArrowheadLength = enum_line[base_data["tail_length"]]  # 화살표의 길이
		set_line.Line.EndArrowheadWidth = enum_line[base_data["tail_width"]]  # 화살표의 넓이
		result = set_line.Name
		return result

	def new_line_for_range_by_cxyxy(self, sheet_name, cxyxy):
		"""
		엑셀에서 좌표는 xy_excel에서 사용하는 x, y축과 다른 의미를 갖는다
		그러니 좌표를 의미하는 cxyxy를 사용하거나 pyxyx를 사용하도록 하자

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param cxyxy: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.draw_border_line_by_cxyxy(sheet_name="", cxyxy=[1,1,3,7])
			<object_name>.draw_border_line_by_cxyxy("", [1,1,3,7])
			<object_name>.draw_border_line_by_cxyxy(sheet_name="sht1", cxyxy=[1,1,3,7])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		new_shape_obj = sheet_obj.Shapes.AddLine(cxyxy[0], cxyxy[1], cxyxy[2], cxyxy[3])
		return new_shape_obj

	def new_line_for_splitted_data(self, xyxy, union_char="#"):
		temp = ""
		old_x = self.x1
		for x in range(self.x1, self.x2 + 1):
			gijun_data = self.read_value_for_cell("", [x, self.y1])
			value = self.read_value_for_cell("", [x, self.y1 + 1])

			if gijun_data:
				self.sheet_obj.Cells(old_x, self.y1 + 2).Value = temp[:-len(union_char)]
				temp = value + union_char
				old_x = x
			else:
				temp = temp + value + union_char
		self.sheet_obj.Cells(old_x, self.y1 + 2).Value = temp[:-len(union_char)]

	def new_nea_sheet(self, input_no):
		for one in range(input_no):
			self.new_sheet_obj()

	def new_range_obj_for_range(self, sheet_name, xyxy):
		"""
		range 객체를 영역으로 만드는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_range_obj(sheet_name="", xyxy="")
			<object_name>.new_range_obj("sht1", [1,1,3,20])
			<object_name>.new_range_obj("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		if x1 == 0 or x2 == 0:
			start = self.change_num_to_char(y1)
			end = self.change_num_to_char(y2)
			changed_address = str(start) + ":" + str(end)
			range_obj = sheet_obj.Columns(changed_address)
		elif y1 == 0 or y2 == 0:
			start = self.change_char_to_num(x1)
			end = self.change_char_to_num(x2)
			changed_address = str(start) + ":" + str(end)
			range_obj = sheet_obj.Rows(changed_address)
		else:
			range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		return range_obj

	def new_range_obj_for_selection(self):
		"""
		선택한 영역의 range 객체를 갖고오는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_range_obj_for_selection()
		"""
		range_obj = self.xlapp.Selection
		return range_obj.Address

	def new_range_obj_for_xxline(self, sheet_name, xx_list):
		"""
		세로줄의 영역을 range객체로 만드는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xx_list: (list) 가로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_range_obj_for_xxline(sheet_name="", xx_list=[3,5])
			<object_name>.get_range_obj_for_xxline("", [1,7])
			<object_name>.get_range_obj_for_xxline(sheet_name="sht1", xx_list=[3,5])
		"""
		new_x = self.check_xx_address(xx_list)
		sheet_obj = self.check_sheet_name(sheet_name)
		result = sheet_obj.Rows(str(new_x[0]) + ':' + str(new_x[1]))
		return result

	def new_range_obj_for_yyline(self, sheet_name, yy_list):
		"""
		가로줄의 영역을 range객체로 만드는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param yy_list: (list) 세로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_range_obj_for_yyline(sheet_name="", yy_list=[2, 4])
			<object_name>.get_range_obj_for_yyline("", [2, 4])
			<object_name>.get_range_obj_for_yyline("sht1", [3,7])
		"""
		new_y = self.check_yy_address(yy_list)
		sheet_obj = self.check_sheet_name(sheet_name)
		result = sheet_obj.Columns(str(new_y[0]) + ':' + str(new_y[1]))
		return result

	def new_rectangle_by_ltwh(self, top, left, width_float, height_float):
		new_shape_obj = self.sheet_obj.Shapes.AddShape(1, left, top, width_float, height_float)
		new_shape_obj.Fill.Transparency = 1
		return new_shape_obj

	def new_rectangle_by_pxywh(self, input_pxywh):
		px, py, pw, ph = input_pxywh
		rectangle_obj = self.sheet_obj.Shapes.AddShape(Type=1, Left=px, Top=py, Width=pw, Height=ph)
		rectangle_obj.Fill.Transparency = 1  # 투명하게
		return rectangle_obj

	def new_rectangle_by_pxyxy(self, input_pxywh):
		sheet_obj = self.new_rectangle_by_pxywh(input_pxywh)
		return sheet_obj

	def new_shape(self, shape_style, color_name, input_value=""):
		pxywh = self.xyxy2_to_pxywh([self.x1, self.y1, self.x2, self.y2])
		check_shape_style = {"circle": 9, "원": 9}
		shape_obj = self.sheet_obj.Shapes.AddShape(check_shape_style[shape_style], pxywh[0], pxywh[1], pxywh[2],
												   pxywh[3])

		shape_obj.Fill.ForeColor.RGB = self.color.change_xcolor_to_rgbint(color_name)
		if input_value:
			shape_obj.TextFrame2.VerticalAnchor = self.varx["shape_font"]["align_v"]
			shape_obj.TextFrame2.HorizontalAnchor = self.varx["shape_font"]["align_h"]
			shape_obj.TextFrame2.TextRange.Font.Bold = self.varx["shape_font"]["bold"]

			shape_obj.TextFrame2.TextRange.Characters.Font.Fill.ForeColor.RGB = self.varx["shape_font"]["color"]
			shape_obj.TextFrame2.TextRange.Characters.Text = input_value
			shape_obj.TextFrame2.TextRange.Characters.Font.Size = self.varx["shape_font"]["size"]

	def new_shape_as_circle_with_number(self, color_name, input_value, font_size=""):
		if font_size: self.varx["font"]["size"] = font_size

		pxywh = self.xyxy2_to_pxywh([self.x1, self.y1, self.x2, self.y2])
		shape_obj = self.sheet_obj.Shapes.AddShape(9, pxywh[0], pxywh[1], pxywh[2], pxywh[3])
		shape_obj.Fill.ForeColor.RGB = self.color.change_xcolor_to_rgbint(color_name)
		shape_obj.TextFrame2.VerticalAnchor = 3
		shape_obj.TextFrame2.HorizontalAnchor = 2
		shape_obj.TextFrame2.TextRange.Font.Bold = self.varx["font"]["bold"]
		shape_obj.TextFrame2.TextRange.Characters.Text = input_value
		shape_obj.TextFrame2.TextRange.Characters.Font.Size = self.varx["font"]["size"]

	def new_shape_as_circle_with_number_for_range(self, sheet_name, xy="", pwh=25, color_name="yel70", input_value=1, font_size=""):
		"""
		원을 만들고, 안에 숫자를 연속적으로 만드는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param pwh: (list) 픽셀의 가로와 세로의 번호
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:param input_value: (any) 입력값
		:param font_size: (int) 폰트의 크기
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_shape_as_circle_with_number(sheet_name="", xy="", pwh=25, color_name="yel70", input_value=1, font_size=15)
			<object_name>.new_shape_as_circle_with_number("", "", 25, "red70", 1, 10)
			<object_name>.new_shape_as_circle_with_number(sheet_name="sht1", xy=[1,3], pwh=25, color_name="yel70", input_value=1, font_size=10)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		if font_size: self.varx["font"]["size"] = font_size

		pxyxy = self.xyxy2_to_pxyxy(xy)
		shape_obj = sheet_obj.Shapes.AddShape(9, pxyxy[0], pxyxy[1], pwh, pwh)
		shape_obj.Fill.ForeColor.RGB = self.color.change_xcolor_to_rgbint(color_name)
		shape_obj.TextFrame2.VerticalAnchor = 3
		shape_obj.TextFrame2.HorizontalAnchor = 2
		shape_obj.TextFrame2.TextRange.Font.Bold = self.varx["font"]["bold"]
		shape_obj.TextFrame2.TextRange.Characters.Text = input_value
		shape_obj.TextFrame2.TextRange.Characters.Font.Size = self.varx["font"]["size"]

	def new_shape_as_pxyxy_for_range(self, sheet_name, pxyxy, shape_no):
		"""
		특정위치에 도형을 만드는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param pxyxy: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param shpae_no: (int) 도형객체의 번호
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_shape_at_pxyxy(sheet_name="", pxyxy="", shape_no=2)
			<object_name>.new_shape_at_pxyxy("", [1,1,3,20], 3)
			<object_name>.new_shape_at_pxyxy("sht1", [1,1,1,20], 2)
		"""
		if isinstance(shape_no, int):
			pass
		elif shape_no in list(self.varx["shape_enum"].keys()):
			shape_no = self.varx["shape_enum"][shape_no]

		sheet_obj = self.check_sheet_name(sheet_name)
		px1, py1, px2, py2 = pxyxy
		shape_obj = sheet_obj.Shapes.AddShape(shape_no, px1, py1, px2, py2)
		return shape_obj

	def new_shape_at_pxyxy(self, pxyxy, shape_no):
		if isinstance(shape_no, int):
			pass
		elif shape_no in list(self.varx["shape_enum"].keys()):
			shape_no = self.varx["shape_enum"][shape_no]

		px1, py1, px2, py2 = pxyxy
		shape_obj = self.sheet_obj.Shapes.AddShape(shape_no, px1, py1, px2, py2)
		return shape_obj

	def new_shape_box_for_same_size_for_range(self, sheet_name, xyxy, line_color="bla", line_thickness="thin"):
		"""
		영역의 테두리와 맞는 사각형 텍스트박스를 만드는데, 투명도가 100%로 설정한 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param line_color: (str) 내부적으로 사용하는 색을 나타내는 문자열
		:param line_thickness: (int) 색의 두께를 나타내는 숫자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_shape_box_for_same_size_with_xyxy(sheet_name="", xyxy="", line_color="bla", line_thickness="thin")
			<object_name>.new_shape_box_for_same_size_with_xyxy("", "", "bla", "thin")
			<object_name>.new_shape_box_for_same_size_with_xyxy(sheet_name="sht1", xyxy=[1,1,3,7], line_color="red", line_thickness="thin")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		sheet_obj = self.check_sheet_name(sheet_name)
		pxywh = self.xyxy2_to_pxywh(sheet_name, xyxy)

		Shpl = sheet_obj.Shapes.AddShape(1, pxywh[0], pxywh[1], pxywh[2], pxywh[3])
		Shpl.Fill.Transparency = 1
		Shpl.Line.ForeColor.RGB = self.color.change_xcolor_to_rgbint(line_color)

		try:
			thickness = self.varx["line"]["check_line_style"][line_thickness]
		except:
			thickness = line_thickness
		Shpl.Line.Weight = thickness

	def new_shape_box_for_same_size_with_xyxy(self, line_color="bla", line_thickness="thin"):
		pxywh = self.xyxy2_to_pxywh()

		Shpl = self.sheet_obj.Shapes.AddShape(1, pxywh[0], pxywh[1], pxywh[2], pxywh[3])
		Shpl.Fill.Transparency = 1
		Shpl.Line.ForeColor.RGB = self.color.change_xcolor_to_rgbint(line_color)

		try:
			thickness = self.varx["line"]["check_line_style"][line_thickness]
		except:
			thickness = line_thickness
		Shpl.Line.Weight = thickness

	def new_shape_by_range(self, sheet_name, xyxy, shape_no):
		"""
		도형객체를 추가하는것

		shape_no : 엑셀에서 정의한 도형의 번호
		xywh : 왼쪽윗부분의 위치에서 너비와 높이
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_shape_for_range(sheet_name="", xyxy="", shape_no=2)
			<object_name>.new_shape_for_range("", [1,1,3,20], 3)
			<object_name>.new_shape_for_range("sht1", [1,1,1,20], 2)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)

		# 도형이 숫자이면 그대로, 문자이면 기본자료에서 찾도록 한다
		if isinstance(shape_no, int):
			pass
		elif shape_no in list(self.varx["shape_enum"].keys()):
			shape_no = self.varx["shape_enum"][shape_no]

		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		xywh = [range_obj.Left, range_obj.Top, range_obj.Width, range_obj.Height]
		shape_obj = sheet_obj.Shapes.Addshape(shape_no, xywh[0], xywh[1], xywh[2], xywh[3])
		return shape_obj

	def new_shape_by_xywh(self, shape_no, input_xywh):
		new_shape_obj = self.sheet_obj.Shapes.Addshape(shape_no, input_xywh[0], input_xywh[1], input_xywh[2],
													   input_xywh[3])
		return new_shape_obj

	def new_shape_by_xywh_for_sheet(self, sheet_name, shape_no, input_xywh):
		"""
		그림을 픽셀크기로 시트에 넣는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param shape_no: (int) 정수 엑셀에서 정의한 도형의 번호
		:param input_xywh: (list) [x, y, width, height], 왼쪽윗부분의 위치에서 너비와 높이
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_shape_by_xywh(sheet_name="", shape_no=35, input_xywh=[1,1,20,30])
			<object_name>.new_shape_by_xywh("", 35, [1,1,20,30])
			<object_name>.new_shape_by_xywh(sheet_name="sht1", shape_no=35, input_xywh=[1,1,20,30])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		new_shape_obj = sheet_obj.Shapes.Addshape(shape_no, input_xywh[0], input_xywh[1], input_xywh[2], input_xywh[3])
		return new_shape_obj

	def new_shape_for_number_circle_by_setup(self, input_no):
		pxywh = self.xyxy2_to_pxywh([self.x1, self.y1, self.x2, self.y2])

		rgb_l1d = self.color.change_xcolor_to_rgb(self.varx["shape"]["color"])
		rgb_int = self.color.change_rgb_to_rgbint(rgb_l1d)

		shape_obj = self.sheet_obj.Shapes.AddShape(9, pxywh[0], pxywh[1], pxywh[2], pxywh[3])
		shape_obj.Fill.ForeColor.RGB = rgb_int
		shape_obj.TextFrame2.VerticalAnchor = self.varx["shape_font"]["align_v"]
		shape_obj.TextFrame2.HorizontalAnchor = self.varx["shape_font"]["align_h"]

		shape_obj.TextFrame2.TextRange.Font.Size = self.varx["shape_font"]["size"]
		shape_obj.TextFrame2.TextRange.Font.Bold = self.varx["shape_font"]["bold"]
		shape_obj.TextFrame2.TextRange.Font.Italic = self.varx["shape_font"]["italic"]
		shape_obj.TextFrame2.TextRange.Font.Name = self.varx["shape_font"]["name"]

		shape_obj.TextFrame2.TextRange.Font.Strikethrough = self.varx["shape_font"]["strikethrough"]
		shape_obj.TextFrame2.TextRange.Font.Subscript = self.varx["shape_font"]["subscript"]
		shape_obj.TextFrame2.TextRange.Font.Superscript = self.varx["shape_font"]["superscript"]
		shape_obj.TextFrame2.TextRange.Font.Alpha = self.varx["shape_font"]["alpha"]
		shape_obj.TextFrame2.TextRange.Font.Underline = self.varx["shape_font"]["underline"]

		rgb2_l1d = self.color.change_xcolor_to_rgb(self.varx["shape_font"]["color"])
		rgb2_int = self.color.change_rgb_to_rgbint(rgb2_l1d)
		shape_obj.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = rgb2_int

		shape_obj.TextFrame2.TextRange.Characters.Text = input_no
		shape_obj.TextFrame2.TextRange.Characters.Font.Size = self.varx["shape_font"]["size"]

	def new_shape_for_number_circle_by_setup_for_range(self, sheet_name, xy="", input_no=1):
		"""
		기본적인 자료를 제외하고, 나머지는 setup자료를 사용한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param input_no: (int) 정수, 입력으로 들어오는 숫자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_shape_for_number_circle_by_setup(sheet_name="", xy="", input_no=2)
			<object_name>.new_shape_for_number_circle_by_setup("", [3,20], 4)
			<object_name>.new_shape_for_number_circle_by_setup("sht1", [1,1], 5)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		pxyxy = self.xyxy2_to_pxyxy(xy)

		rgb_l1d = self.color.change_xcolor_to_rgb(self.varx["shape"]["color"])
		rgb_int = self.color.change_rgb_to_rgbint(rgb_l1d)

		shape_obj = sheet_obj.Shapes.AddShape(9, pxyxy[0], pxyxy[1], self.varx["shape"]["width"],
										 self.varx["shape"]["height"])
		shape_obj.Fill.ForeColor.RGB = rgb_int
		shape_obj.TextFrame2.VerticalAnchor = self.varx["shape_font"]["align_v"]
		shape_obj.TextFrame2.HorizontalAnchor = self.varx["shape_font"]["align_h"]

		shape_obj.TextFrame2.TextRange.Font.Size = self.varx["shape_font"]["size"]
		shape_obj.TextFrame2.TextRange.Font.Bold = self.varx["shape_font"]["bold"]
		shape_obj.TextFrame2.TextRange.Font.Italic = self.varx["shape_font"]["italic"]
		shape_obj.TextFrame2.TextRange.Font.Name = self.varx["shape_font"]["name"]

		shape_obj.TextFrame2.TextRange.Font.Strikethrough = self.varx["shape_font"]["strikethrough"]
		shape_obj.TextFrame2.TextRange.Font.Subscript = self.varx["shape_font"]["subscript"]
		shape_obj.TextFrame2.TextRange.Font.Superscript = self.varx["shape_font"]["superscript"]
		shape_obj.TextFrame2.TextRange.Font.Alpha = self.varx["shape_font"]["alpha"]
		shape_obj.TextFrame2.TextRange.Font.Underline = self.varx["shape_font"]["underline"]

		rgb2_l1d = self.color.change_xcolor_to_rgb(self.varx["shape_font"]["color"])
		rgb2_int = self.color.change_rgb_to_rgbint(rgb2_l1d)
		shape_obj.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = rgb2_int

		shape_obj.TextFrame2.TextRange.Characters.Text = input_no
		shape_obj.TextFrame2.TextRange.Characters.Font.Size = self.varx["shape_font"]["size"]

	def new_shape_for_range(self, sheet_name, xy, size=[25, 25], shape_style="circle", color_name="yel70", input_value=""):
		"""
		원을 만들고, 안에 숫자를 연속적으로 만드는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_shape(sheet_name="", xy="", size=[25, 25], shape_style="circle", color_name="yel70", input_value="")
			<object_name>.new_shape("", "", size=[20, 25], shape_style="circle", color_name="yel70", input_value="")
			<object_name>.new_shape(sheet_name="sht1", xy=[2,3], size=[25, 35], shape_style="circle", color_name="red70", input_value="")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		pxyxy = self.xyxy2_to_pxyxy(xy)
		check_shape_style = {"circle": 9, "원": 9}

		shape_obj = sheet_obj.Shapes.AddShape(check_shape_style[shape_style], pxyxy[0], pxyxy[1], size[0], size[1])

		shape_obj.Fill.ForeColor.RGB = self.color.change_xcolor_to_rgbint(color_name)
		if input_value:
			shape_obj.TextFrame2.VerticalAnchor = self.varx["shape_font"]["align_v"]
			shape_obj.TextFrame2.HorizontalAnchor = self.varx["shape_font"]["align_h"]
			shape_obj.TextFrame2.TextRange.Font.Bold = self.varx["shape_font"]["bold"]

			shape_obj.TextFrame2.TextRange.Characters.Font.Fill.ForeColor.RGB = self.varx["shape_font"]["color"]
			shape_obj.TextFrame2.TextRange.Characters.Text = input_value
			shape_obj.TextFrame2.TextRange.Characters.Font.Size = self.varx["shape_font"]["size"]

	def new_shape_line(self, color_name, thickness, line_style, transparency, head_dic, tail_dic=""):
		enum_line = self.varx["end_style_vs_enum"]
		base_data = self.varx["dic_base_cell_data"]
		# 기본자료에 입력받은값을 update하는것이다

		base_data.update(input)
		set_line = self.sheet_obj.Shapes.AddLine(self.x1, self.y1, self.x2, self.y2)
		set_line.Select()

		set_line.Line.ForeColor.RGB = self.color.change_xcolor_to_rgbint(color_name)
		set_line.Line.DashStyle = line_style
		set_line.Line.Weight = thickness
		set_line.Line.Transparency = transparency

		if head_dic:
			# 엑셀에서는 Straight Connector 63의 형태로 이름이 자동적으로 붙여진다
			set_line.Line.BeginArrowheadStyle = enum_line[base_data[head_dic["style"]]]
			set_line.Line.BeginArrowheadLength = enum_line[base_data[head_dic["height"]]]
			set_line.Line.BeginArrowheadWidth = enum_line[base_data[head_dic["width"]]]

		if tail_dic:
			set_line.Line.EndArrowheadStyle = enum_line[base_data[tail_dic["style"]]]  # 화살표의 머리의 모양
			set_line.Line.EndArrowheadLength = enum_line[base_data[tail_dic["height"]]]  # 화살표의 길이
			set_line.Line.EndArrowheadWidth = enum_line[base_data[tail_dic["width"]]]  # 화살표의 넓이
		return set_line

	def new_shape_line_by_pxyxy(self, pxyxy, color_name):
		line_obj = self.sheet_obj.Shapes.AddLine(pxyxy[0], pxyxy[1], pxyxy[2],
												 pxyxy[3]).Select()
		self.xlapp.Selection.ShapeRange.Line.ForeColor.RGB = self.color.change_xcolor_to_rgbint(color_name)
		self.xlapp.Selection.ShapeRange.Line.Weight = 5

	def new_shape_line_by_pxyxy_for_range(self, sheet_name, pxyxy, color_name):
		"""
		선택영역에서 선을 긋는것
		pixel을 기준으로 선긋기
		선을 그을때는 위치와 넓이 높이로 긋는데, xyxy2_to_pxyxy을 사용하면 셀위치를 그렇게 바꾸게 만든다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param rgb_list: (list) rgb값을 나타내는 리스트
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_shape_line_by_pxyxy(sheet_name="", pxyxy="", color_name="yel70")
			<object_name>.new_shape_line_by_pxyxy("", [1,1,3,4], color_name="red50")
			<object_name>.new_shape_line_by_pxyxy(sheet_name="sht1", pxyxy=[1,1,3,4], color_name="yel70")
		"""

		sheet_obj = self.check_sheet_name(sheet_name)

		line_obj = sheet_obj.Shapes.AddLine(pxyxy[0], pxyxy[1], pxyxy[2], pxyxy[3]).Select()
		self.xlapp.Selection.ShapeRange.Line.ForeColor.RGB = self.color.change_xcolor_to_rgbint(color_name)
		self.xlapp.Selection.ShapeRange.Line.Weight = 5

	def new_shape_line_for_range(self, sheet_name, xyxy, color_name="yel70", thickness=3, line_style=2, transparency=0.8, head_dic="", tail_dic=""):
		"""
		선택영역에서 선을 긋는것
		선긋기를 좀더 상세하게 사용할수 있도록 만든것
		밐의 base_data의 값들을 이용해서 입력하면 된다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:param thickness: (int) 선의 두께
		:param line_style: (str) 선의 스타일, (점선, 실선등)
		:param transparency: (float) 0부터 1사이의 값
		:param head_dic: (dic) 해드의 형태를 나타내는 사전형태의것
		:param tail_dic: (dic) tail의 형태를 나타내는 사전형태의것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_shape_line_for_range(sheet_name="", xyxy="", color_name="yel70", thickness=3, line_style=2, transparency=0.8, head_dic="", tail_dic="")
			<object_name>.new_shape_line_for_range("", "", "yel70", 3, 2, 0.8, "", "")
			<object_name>.new_shape_line_for_range(sheet_name="sht1", xyxy="", color_name="yel70", thickness=3, line_style=2, transparency=0.8, head_dic="", tail_dic="")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		enum_line = self.varx["end_style_vs_enum"]
		base_data = self.varx["dic_base_cell_data"]
		# 기본자료에 입력받은값을 update하는것이다

		base_data.update(input)
		sheet_obj = self.check_sheet_name(sheet_name)
		set_line = sheet_obj.Shapes.AddLine(xyxy[0], xyxy[1], xyxy[2], xyxy[3])
		set_line.Select()

		set_line.Line.ForeColor.RGB = self.color.change_xcolor_to_rgbint(color_name)
		set_line.Line.DashStyle = line_style
		set_line.Line.Weight = thickness
		set_line.Line.Transparency = transparency

		if head_dic:
			# 엑셀에서는 Straight Connector 63의 형태로 이름이 자동적으로 붙여진다
			set_line.Line.BeginArrowheadStyle = enum_line[base_data[head_dic["style"]]]
			set_line.Line.BeginArrowheadLength = enum_line[base_data[head_dic["height"]]]
			set_line.Line.BeginArrowheadWidth = enum_line[base_data[head_dic["width"]]]

		if tail_dic:
			set_line.Line.EndArrowheadStyle = enum_line[base_data[tail_dic["style"]]]  # 화살표의 머리의 모양
			set_line.Line.EndArrowheadLength = enum_line[base_data[tail_dic["height"]]]  # 화살표의 길이
			set_line.Line.EndArrowheadWidth = enum_line[base_data[tail_dic["width"]]]  # 화살표의 넓이
		return set_line

	def new_shape_line_for_range_with_detail(self, sheet_name, xyxy, position="", line_style="_", thickness="thin", color_name="yel70", head_setup=False, tail_setup=False):
		"""
		선택영역에서 선을 긋는것
		선긋기를 좀더 상세하게 사용할수 있도록 만든것
		밐의 base_data의 값들을 이용해서 입력하면 된다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param position: (str) 입력으로 들어오는 텍스트, 위치를 나타내는 문자
		:param line_style: (str) 선의 스타일, (점선, 실선등)
		:param thickness: (int) 선의 두께
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:param head_setup: (bool) head를 나타낼것인지 아닌지 선택하는것
		:param tail_setup: (bool) tail을 나타낼것인지 아닌지 선택하는것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_shape_line_for_range_with_detail(sheet_name="", xyxy="", position="", line_style="_", thickness="thin", color_name="yel70", head_setup=False, tail_setup=False)
			<object_name>.new_shape_line_for_range_with_detail("", "", "", "_", "thin", "yel70", False, False)
			<object_name>.new_shape_line_for_range_with_detail(sheet_name="sht1", xyxy=[1,1,4,5], position="", line_style="_", thickness="thin", color_name="yel70", head_setup=False, tail_setup=False)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		default_dic = {"position": [7, 8, 9, 10], "line_style": "-", "thickness": "t-1", "color": "bla"}
		temp_dic = self.check_line_style([position, line_style, thickness, color_name])
		default_dic.update(temp_dic)

		for abc in default_dic["position"]:
			range_obj.Borders(abc).Color = self.color.change_xcolor_to_rgbint(default_dic["color"])
			range_obj.Borders(abc).Weight = default_dic["thickness"]
			range_obj.Borders(abc).LineStyle = default_dic["line_style"]

		enum_line = self.varx["end_style_vs_enum"]
		base_data = self.varx["dic_base_cell_data"]
		# 기본자료에 입력받은값을 update하는것이다
		sheet_obj = self.check_sheet_name("")
		base_data.update(input)
		sheet = self.check_sheet_name(base_data["sheet_name"])
		set_line = sheet_obj.Shapes.AddLine(base_data["xyxy"][0], base_data["xyxy"][1], base_data["xyxy"][2],base_data["xyxy"][3])
		set_line.Select()
		set_line.Line.ForeColor.RGB = base_data["color"]
		set_line.Line.DashStyle = enum_line[base_data["line_style"]]
		set_line.Line.Weight = base_data["thickness"]
		set_line.Line.Transparency = base_data["transparency"]

		# 엑셀에서는 Straight Connector 63의 형태로 이름이 자동적으로 붙여진다
		set_line.Line.BeginArrowheadStyle = enum_line[base_data["head_style"]]
		set_line.Line.BeginArrowheadLength = enum_line[base_data["head_length"]]
		set_line.Line.BeginArrowheadWidth = enum_line[base_data["head_width"]]
		set_line.Line.EndArrowheadStyle = enum_line[base_data["tail_style"]]  # 화살표의 머리의 모양
		set_line.Line.EndArrowheadLength = enum_line[base_data["tail_length"]]  # 화살표의 길이
		set_line.Line.EndArrowheadWidth = enum_line[base_data["tail_width"]]  # 화살표의 넓이
		result = set_line.Name
		return set_line

	def new_shape_obj_by_name(self, sheet_name, shape_no):
		"""
		도형의 번호를 기준으로 도형의 객체를 갖고오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param shape_no: (int) 정수 도형의 번호
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_shape_obj_by_no_or_name(sheet_name="", shape_no=3)
			<object_name>.new_shape_obj_by_no_or_name("", 7)
			<object_name>.new_shape_obj_by_no_or_name("sht1", 7)
		"""

		sheet_obj = self.check_sheet_name(sheet_name)

		if isinstance(shape_no, str):
			shape_name = self.check_shape_name(sheet_name, shape_no)
			shape_obj = sheet_obj.Shapes(shape_name)
		elif isinstance(shape_no, int):
			shape_obj = sheet_obj.Shapes(shape_no)
		return shape_obj

	def new_shape_obj_by_no(self, sheet_name, shape_no):
		"""
		도형번호를 입력하면 도형의 객체를 돌려주는 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param shape_no: (int) 정수 도형의 번호
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_shape_obj_by_no(sheet_name="", shape_no=3)
			<object_name>.new_shape_obj_by_no("", 7)
			<object_name>.new_shape_obj_by_no("sht1", 7)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)

		if isinstance(shape_no, str):
			shape_name = self.check_shape_name(sheet_name, shape_no)
			shape_obj = sheet_obj.Shapes(shape_name)
		elif isinstance(shape_no, int):
			shape_obj = sheet_obj.Shapes(shape_no)
		return shape_obj

	def new_sheet(self):
		"""
		새로운 시트 추가하기

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_sheet()
		"""
		self.new_sheet_with_name("")

	def new_sheet_obj(self, sheet_name):
		"""
		입력한 시트이름의 시트객체를 돌려주는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_sheet_obj(sheet_name="")
			<object_name>.new_sheet_obj("sht1")
			<object_name>.new_sheet_obj("")
		"""
		return self.check_sheet_name(sheet_name)

	def new_sheet_obj_for_activesheet(self):
		"""
		현재 활성화된 시트를 객체형식으로 돌려주는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_sheet_obj_for_activesheet()
		"""
		sheet_name = self.xlapp.ActiveSheet.Name
		sheet_obj = self.check_sheet_name(sheet_name)
		return sheet_obj

	def new_sheet_with_name(self, sheet_name):
		"""
		시트하나 추가
		단, 이름을 확인해서 같은것이 있으면, 그냥 넘어간다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_sheet_with_name(sheet_name="")
			<object_name>.new_sheet_with_name("sht1")
			<object_name>.new_sheet_with_name("")
		"""
		if sheet_name == "":
			self.xlbook.Worksheets.Add()
		else:
			sheets_name = self.get_sheet_names()
			if sheet_name in sheets_name:
				self.util.messagebox("같은 시트이름이 있읍니다")
			else:
				self.xlbook.Worksheets.Add()
				old_name = self.xlbook.ActiveSheet.Name
				self.xlbook.Worksheets(old_name).Name = sheet_name

	def new_sheet_with_nea(self, input_no):
		"""
		n개의 새로운 시트 추가하기

		:param input_no: (int) 정수, 입력으로 들어오는 숫자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_sheet_with_nea(input_no=3)
			<object_name>.new_sheet_with_nea(5)
			<object_name>.new_sheet_with_nea(7)
		"""
		for one in range(input_no):
			self.new_sheet_with_name("")

	def new_textbox_at_pxyxy(self, x, y, width_float, height_float, text):
		# 텍스트 상자 추가 및 텍스트 입력
		textbox = self.sheet_obj.Shapes.AddTextbox(1, x, y, width_float, height_float)
		textbox.TextFrame.Characters().Text = text

	def new_textbox_at_pxyxy_for_range(self, sheet_name, x=3, y=7, width_float=12.4, height_float=8.8, text="입력값1"):
		"""
		텍스트박스를 입력받은 픽셀의 영역에 만드는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param x: (int) 정수, x를 나타내는 가로줄의 번호, row의 숫자번호
		:param y: (int) 정수, 엑셀의 세로열(column) 번호를 나타내는것
		:param width_float: (int) 넓이를 나타내는 정수
		:param height_float: (int) 높이를 나타내는 정수
		:param text: (str) 입력으로 들어오는 텍스트, 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_textbox_at_pxyxy(sheet_name="", x=3, y=7, width_float=12.4, height_float=8.8, text="입력값1")
			<object_name>.new_textbox_at_pxyxy("", 3, 7, 12.4, height_float=8.8, text="입력값1")
			<object_name>.new_textbox_at_pxyxy(sheet_name="sht1", x=3, y=7, width_float=12.4, height_float=8.8, text="입력값1")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)

		# 텍스트 상자 추가 및 텍스트 입력
		textbox = sheet_obj.Shapes.AddTextbox(1, x, y, width_float, height_float)
		textbox.TextFrame.Characters().Text = text

	def new_triangle(self, xyxy="", per=100, reverse=1, size=100):
		"""
		직각삼각형
		정삼각형에서 오른쪽이나 왼쪽으로 얼마나 더 간것인지
		100이나 -100이면 직삼각형이다
		사각형은 왼쪽위에서 오른쪽 아래로 만들어 진다

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param per: (int) 삼각형을 만드는 형태일때, 직삼각형을 나타내는 정도를 나타내는 숫자
		:param reverse: (bool) 삼각형이 위아래를 바꿀것인지를 선택하는 것
		:param size: (int) 정수 크기를 나타내는 숫자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.draw_triangle(xyxy="", per=100, reverse=1, size=100)
			<object_name>.draw_triangle("")
			<object_name>.draw_triangle(xyxy=[1,1,5,7], per=200)
		"""
		x1, y1, x2, y2 = xyxy
		# width = x2 - x1
		# height = y2 - y1
		# lt = [x1, y1] # left top
		lb = [x2, y1]  # left bottom
		rt = [x1, y2]  # right top
		rb = [x2, y2]  # right bottom
		# tm = [x1, int(y1 + width / 2)] # 윗쪽의 중간
		# lm = [int(x1 + height / 2), y1] # 윗쪽의 중간
		# rm = [int(x1 + height / 2), y1] # 윗쪽의 중간
		# bm = [x2, int(y1 + width / 2)] # 윗쪽의 중간
		# center = [int(x1 + width / 2), int(y1 + height / 2)]

		result = [lb, rb, rt]
		return result

	def new_workbook_filter_by_same_values(self, sheet_name, xyxy, line_index=3, first_is_title_or_not=True, folder_name="D:\\temp\\abc.xlsx"):
		"""
		선택한 영역의 몇번째 줄이 같은것들만 묶어서 엑셀화일 만들기
		1) 저장활 플더를 확인
		2) 첫즐에 제목이 있는지 아닌지에 따라서 자료영역을 바꾸는 것
		3) 읽어온 자료
		4) 자료증에서 어떤 줄을 기준으로 그룹화 하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param line_index: (int) 정수 정수
		:param first_is_title_or_not: (bool) 첫줄이 각 컬럼들의 이름을 나타내는지를 설정하는것
		:param folder_name: (str) 폴더의 이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_workbook_filter_by_same_values(sheet_name="", xyxy="", line_index=3, first_is_title_or_not=True, folder_name="D:\\temp\\abc.xlsx")
			<object_name>.new_workbook_filter_by_same_values("", "", 3, True, "D:\\temp\\abc.xlsx")
			<object_name>.new_workbook_filter_by_same_values(sheet_name="sht1", xyxy="", line_index=3, first_is_title_or_not=True, folder_name="D:\\temp\\abc.xlsx")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		self.util.make_folder(folder_name)  # 1
		sheet_obj_0 = sheet_obj = self.check_sheet_name(sheet_name)
		# 2
		if first_is_title_or_not:
			new_range = [1 + 1, y1, x2, y2]
		l2d = self.read_value_for_range(sheet_name, new_range)  # 3
		grouped_data = self.util.group_l2d_by_index(l2d, line_index)  # 4
		startx = 1
		count = 1
		for one_group in grouped_data:
			range_2 = self.concate_range_n_line_no(new_range, [start_x, start_x + len(one_group) - 1])
			if first_is_title_or_not:
				self.select_multi_range(sheet_obj_0, [[x1, y1, x1, y2], range_2])
			else:
				self.select_multi_range(sheet_obj_0, [range_2])
			self.xlapp.selection.Copy()
			self.new_workbook("")
			sheet_obj = self.check_sheet_name("")
			sheet_obj.Cells(1, 1).Select()
			sheet_obj.Paste()
			self.save(folder_name + "\\" + str(one_group[0][line_index]) + "_" + str(count) + ".xlsx")
			self.close_active_workbook()
			start_x = start_x + len(one_group)
			count = count + 1

	def new_xy_list_for_box_style(self, xyxy):
		"""
		좌표를 주면, 맨끝만 나터내는 좌표를 얻는다

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.new_xy_list_for_box_style(xyxy="")
			<object_name>.new_xy_list_for_box_style([1,1,3,20])
		"""
		temp_1 = []
		for x in [xyxy[0], xyxy[2]]:
			temp = [[x, y] for y in range(xyxy[1], xyxy[3] + 1)]
			temp_1.append(temp)

		temp_2 = []
		for y in [xyxy[1], xyxy[3]]:
			temp = [[x, y] for x in range(xyxy[0], xyxy[2] + 1)]
			temp_2.append(temp)

		result = [temp_1[0], temp_2[1], temp_1[1], temp_2[0]]
		return result

	def numberformat_for_xline(self, sheet_name, input_xno, style="style1"):
		"""
		열을 기준으로 셀의 속성을 설정하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_xno: (int) 정수, x를 나타내는 가로줄의 번호, row의 숫자번호
		:param style: (str) 입력으로 들어오는 텍스트, 모양을 나타내는 스타일을 넣는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_numberformat_for_xline(sheet_name="", input_xno=1, type1='general')
			<object_name>.set_numberformat_for_xline(sheet_name="", input_xno=4, type1='number')
			<object_name>.set_numberformat_for_xline(sheet_name="", input_xno=7, type1='date')
		"""
		self.set_numberformat_for_xxline(sheet_name, input_xno, style)

	def numberformat_for_xxline(self, sheet_name, input_xno, style="style1"):
		"""
		set_xxline_numberformat(sheet_name="", input_xno, style)
		각 열을 기준으로 셀의 속성을 설정하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_xno: (int) 정수, x를 나타내는 가로줄의 번호, row의 숫자번호
		:param style: (str) 입력으로 들어오는 텍스트, 모양을 나타내는 스타일을 넣는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_xxline_numberformat(sheet_name="", input_xno=1, style='general')
			<object_name>.set_xxline_numberformat(sheet_name="", input_xno=4, style='number')
			<object_name>.set_xxline_numberformat(sheet_name="", input_xno=7, style='date')
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1 = self.check_xy_address(input_xno)
		x = self.change_char_to_num(x1)
		if style == 1:  # 날짜의 설정
			sheet_obj.Columns(x).NumberFormatLocal = "mm/dd/"
		elif style == 2:  # 숫자의 설정
			sheet_obj.Columns(x).NumberFormatLocal = "_-* #,##0.00_-;-* #,##0.00_-;_-* '-'_-;_-@_-"
		elif style == 3:  # 문자의 설정
			sheet_obj.Columns(x).NumberFormatLocal = "@"

	def numberproperty_for_range(self, sheet_name, xyxy, type1="style1"):
		"""
		좀더 사용하기 쉽도록 변경이 필요

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param type1: (str) 입력으로 들어오는 텍스트, 숫자를 표현하는 서식을 설정
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_numberproperty_for_range(sheet_name="", xyxy="", type1='general')
			<object_name>.set_numberproperty_for_range(sheet_name="", xyxy="", type1='number')
			<object_name>.set_numberproperty_for_range(sheet_name="", xyxy="", type1='date')
		"""
		if type1 == 'general' or type1 == '':
			result = "#,##0.00_ "
		elif type1 == 'number':
			result = "US$""#,##0.00"
		elif type1 == 'account':
			result = "_-""US$""* #,##0.00_ ;_-""US$""* -#,##0.00 ;_-""US$""* ""-""??_ ;_-@_ "
		elif type1 == 'date':
			result = "mm""/""dd""/""xx"
		elif type1 == 'datetime':
			result = "xxxx""-""m""-""d h:mm AM/PM"
		elif type1 == 'percent':
			result = "0.00%"
		elif type1 == 'bunsu':
			result = "# ?/?"
		elif type1 == 'jisu':
			result = "0.00E+00"
		elif type1 == 'text':
			result = "@"
		elif type1 == 'etc':
			result = "000-000"
		elif type1 == 'other':
			result = "$#,##0.00_);[빨강]($#,##0.00)"
		else:
			result = type1  # 만약 아무것도 해당이 않된다면, 그냥 사용자가 서식을 정의한 것이다
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		r1c1 = self.xyxy2_to_r1c1([x1, y1, x2, y2])
		range_obj = sheet_obj.Range(r1c1)
		range_obj.NumberFormat = result

	def open_file(self, input_filename=""):
		"""
		엑셀화일 열기

		:param input_filename: (str) 화일의 이름을 나타내는 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.open_file(input_filename="D:\\my_file.xlsx")
			<object_name>.open_file("D:\\my_file.xlsx")
			<object_name>.open_file("D:\\my_file2.xlsx")
		"""
		self.new_workbook(input_filename)

	def paint(self, color_name):
		"""
			현재 설정된 영역(range_obj)의 배경색을 지정한 색상으로 칠함

			:param color_name: (str) 색상 이름 (xcolor 형식)
			:return: None
			"""
		rgb_int = self.color.change_xcolor_to_rgbint(color_name)
		self.range_obj.Interior.Color = rgb_int

	def paint_2n_xline(self, color_name):
		for no in range(self.x1, self.x2, 2):
			self.set_range([no, self.y1, no, self.y2])
			self.paint(color_name)

	def paint_bar(self, color_value):
		self.range_obj.FormatConditions.AddDatabar()
		self.range_obj.FormatConditions(1).NegativeBarFormat.ColorType = 0  # xlDataBarColor =0
		self.range_obj.FormatConditions(1).NegativeBarFormat.Color.Color = color_value
		self.range_obj.FormatConditions(1).NegativeBarFormat.Color.TintAndShade = 0

	def paint_bar_for_range(self, sheet_name, xyxy, color_value=255):
		"""
		영역안에 색으로된 바를 만드는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_value:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_bar(sheet_name="", xyxy="", color_value=210)
			<object_name>.paint_bar("", [1,1,3,20], 123)
			<object_name>.paint_bar("sht1", [1,1,1,20], 145)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.FormatConditions.AddDatabar()
		range_obj.FormatConditions(1).NegativeBarFormat.ColorType = 0  # xlDataBarColor =0
		range_obj.FormatConditions(1).NegativeBarFormat.Color.Color = color_value
		range_obj.FormatConditions(1).NegativeBarFormat.Color.TintAndShade = 0

	def paint_by_any_color_for_range(self, sheet_name, xyxy, color_name):
		"""
		셀의 배경색을 color_name형식의 색으로 칠하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_by_any_color_for_range(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.paint_by_any_color_for_range("sht1", [1,1,12,23], "red23")
			<object_name>.paint_by_any_color_for_range("", [3,3,5,7], "gra34")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		rgb_int = self.color.change_xcolor_to_rgbint(color_name)
		range_obj.Interior.Color = rgb_int

	def paint_by_hsl(self, input_hsl):
		"""
			현재 설정된 영역의 배경색을 HSL 값으로 설정함

			:param input_hsl: (list/tuple) [H, S, L] 형태의 값
			:return: None
			"""
		self.range_obj.Interior.Color = self.color.change_hsl_to_rgbint(input_hsl)

	def paint_by_hsl_for_range(self, sheet_name, xyxy, input_hsl):
		"""
		셀을 hsl값으로 색칠하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_hsl:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_by_hsl(sheet_name="", xyxy="", input_hsl=[75, 88, 95])
			<object_name>.paint_by_hsl("", [1,1,3,20],[75, 88, 95])
			<object_name>.paint_by_hsl("sht1", [1,1,1,20],input_hsl=[123, 122, 105])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		range_obj.Interior.Color = self.color.change_hsl_to_rgbint(input_hsl)

	def paint_by_rgb(self, input_rgb):
		"""
			현재 설정된 영역의 배경색을 RGB 값으로 설정함

			:param input_rgb: (list) [R, G, B] 형태의 리스트
			:return: None
			"""
		self.range_obj.Interior.Color = self.color.change_rgb_to_rgbint(input_rgb)

	def paint_by_rgb_for_range(self, sheet_name, xyxy, input_rgb):
		"""
		영역에 색깔을 입힌다 엑셀에서의 색깔의 번호는 아래의 공식처럼 만들어 진다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_by_rgb(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.paint_by_rgb("", "", "yel70")
			<object_name>.paint_by_rgb("sht1", "", "red50")
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		range_obj.Interior.Color = self.change_rgb_to_rgbint(input_rgb)

	def paint_cell(self, sheet_name, xyxy, color_name):
		"""
		셀의 배경색을 color_name형식으로 칠하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.paint_cell("sht1", [1,1,12,23], "red23")
			<object_name>.paint_cell("", [3,3,5,7], "gra34")
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Interior.Color = self.color.change_xcolor_to_rgbint(color_name)

	def paint_cell_as_gradation_by_color_n_position(self, input_style, input_obj="object1", input_bg_color="red50", input_l2d=[[1, 2], [4, 5]]):
		"""
		여러가지색을 정하면서 색의 가장 진한 위치를 0~100사이에서 정하는 것

		:param input_style: (str) 스타일을 나타내는 문자열
		:param input_obj: (object) 객체,
		:param input_bg_color: 백그라운드 색
		:param input_l2d: (list) 2차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_as_gradation_by_color_n_position(input_style="style0", input_obj="object1", input_bg_color="red50", input_l2d=[[1, 2], [4, 5]])
			<object_name>.paint_cell_as_gradation_by_color_n_position("style1","obj1", "red40", [[1, 2], [4, 5]])
			<object_name>.paint_cell_as_gradation_by_color_n_position(input_style="style1", input_obj="obj23", input_bg_color="red40", input_l2d=[[1, 2], [4, 5]])
		"""
		style_dic = {"ver": 2, "hor": 1, "cor": 5, "cen": 7, "dow": 4, "up": 3, "mix": -2, }
		input_obj.Fill.ForeColor.RGB = self.color.change_xcolor_to_rgbint(input_bg_color)
		input_l2d = self.check_input_data(input_l2d)

		obj_fill = input_obj.Fill
		obj_fill.OneColorGradient(style_dic[input_style], 1, 1)

		for index, l1d in enumerate(input_l2d):
			rgbint = self.color.change_xcolor_to_rgbint(l1d[0])
			obj_fill.GradientStops.Insert(rgbint, l1d[1] / 100)

	def paint_cell_by_56color(self, sheet_name, xy, input_56color):
		"""
		선택 셀에 색깔을 넣는다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param input_56color: 엑셀기본 56색의 번호
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_by_56color(sheet_name="", xy="", input_56color=12)
			<object_name>.paint_cell_by_56color("", "", 12)
			<object_name>.paint_cell_by_56color(sheet_name="sht1", xy=[3,3], input_56color=5)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		xyxy = self.change_any_address_to_xyxy(xy)
		sheet_obj.Cells(xyxy[0], xyxy[1]).Interior.ColorIndex = int(input_56color)

	def paint_cell_by_same_with_input_value(self, input_value, color_name):
		rgbint = self.color.change_any_color_to_rgbint(color_name)
		for x in range(self.x1, self.x2 + 1):
			for y in range(self.y1, self.y2 + 1):
				value = self.sheet_obj.Cells(x, y).Value2
				if input_value in value:
					self.sheet_obj.Cells(x, y).Interior.Color = rgbint

	def paint_cell_for_differ_value_in_two_xyxy(self, input_l2d_1, input_l2d_2, colored_tf):
		rgbint = self.color.change_any_color_to_rgbint("red++")
		result = []
		for l1d, ix in enumerate(input_l2d_1):
			for one_data, iy in enumerate(l1d):
				if input_l2d_1[ix][iy] == input_l2d_2[ix][iy]:
					pass
				else:
					result.append([ix + 1, iy + 1])
					if colored_tf:
						self.sheet_obj.Cells(ix + 1, iy + 1).Interior.Color = rgbint

	def paint_cell_for_having_space(self, color_name):
		rgbint = self.color.change_any_color_to_rgbint(color_name)
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = self.sheet_obj.Cells(x, y).Value
			com = re.compile(r"^\s+")
			if one_value != None:
				if com.search(one_value):
					self.sheet_obj.Cells(x, y).Interior.Color = rgbint

	def paint_cell_for_max_value_in_each_xline(self, color_name):
		rgbint = self.color.change_any_color_to_rgbint(color_name)
		all_data = self.read()
		if not (self.x1 == self.x2 and self.y1 == self.y2):
			for line_no in range(len(all_data)):
				line_data = all_data[line_no]
				filtered_list = list(filter(lambda x: isinstance(x, int) or isinstance(x, float), line_data))
				if filtered_list == []:
					pass
				else:
					max_value = max(filtered_list)
					x_location = self.x1 + line_no
					for no in range(len(line_data)):
						y_location = self.y1 + no
						if (line_data[no]) == max_value:
							self.sheet_obj.Cells(x_location,
												 y_location).Interior.Color = self.color.change_any_color_to_rgbint(
								color_name)
		else:
			print("Please re-check selection area")

	def paint_cell_for_max_value_in_each_yline(self):
		rgbint = self.color.change_any_color_to_rgbint(16)
		all_data = self.read()
		if not (self.y1 == self.y2 and self.x1 == self.x2):
			for line_no in range(len(all_data)):
				line_data = all_data[line_no]
				filtered_list = list(filter(lambda x: isinstance(x, int) or isinstance(x, float), line_data))
				if filtered_list == []:
					pass
				else:
					max_value = max(filtered_list)
					y_location = self.y1 + line_no
					for no in range(len(line_data)):
						x_location = self.x1 + no
						if (line_data[no]) == max_value:
							self.sheet_obj.Cells(y_location, x_location).Interior.Color = rgbint
		else:
			print("Please re-check selection area")

	def paint_cell_for_min_value_in_each_xline(self, color_name):
		rgbint = self.color.change_any_color_to_rgbint(color_name)
		all_data = self.read()
		if not (self.x1 == self.x2 and self.y1 == self.y2):
			for line_no in range(len(all_data)):
				line_data = all_data[line_no]
				filtered_list = list(filter(lambda x: isinstance(x, int) or isinstance(x, float), line_data))
				if filtered_list == []:
					pass
				else:
					max_value = min(filtered_list)
					x_location = self.x1 + line_no
					for no in range(len(line_data)):
						y_location = self.y1 + no
						if (line_data[no]) == max_value:
							self.sheet_obj.Cells(x_location, y_location).Interior.Color = rgbint
		else:
			print("Please re-check selection area")

	def paint_cell_for_range_by_hsl(self, sheet_name, xyxy, input_hsl):
		"""
		셀을 hsl값으로 색칠하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_hsl:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_by_hsl(sheet_name="", xyxy="", input_hsl=[75, 88, 95])
			<object_name>.paint_cell_by_hsl("", [1,1,3,20],[75, 88, 95])
			<object_name>.paint_cell_by_hsl("sht1", [1,1,1,20],input_hsl=[123, 122, 105])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		rgb = self.color.change_hsl_to_rgb(input_hsl)
		self.paint_cell_by_rgb(sheet_name, xyxy, rgb)

	def paint_cell_for_range_by_rgb(self, sheet_name, xyxy, input_rgb):
		"""
		셀의 배경색을 rgb를 기준으로 칠한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_rgb: rgb형식
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_by_rgb(sheet_name="", xyxy="", input_rgb=[123, 122, 105])
			<object_name>.paint_cell_by_rgb("", [1,1,3,20],input_rgb=[123, 122, 105])
			<object_name>.paint_cell_by_rgb("sht1", [1,1,1,20],input_rgb=[123, 122, 105])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Interior.Color = self.color.change_rgb_to_rgbint(input_rgb)

	def paint_cell_for_range_by_same_with_input_value(self, sheet_name, xyxy, input_value, color_name):
		"""
		영역안에 입력받은 글자와 같은것이 있으면 색칠하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (any) 입력값
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_for_range_by_same_with_input_value(sheet_name="", xyxy="", input_value="입력값", color_name="yel70")
			<object_name>.paint_cell_for_range_by_same_with_input_value("", "", "입력값", "yel70")
			<object_name>.paint_cell_for_range_by_same_with_input_value(sheet_name="sht1", xyxy="", input_value="입력값123", color_name="yel70")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_obj.Cells(x, y).Value2
				if input_value in value:
					sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint(color_name)

	def paint_cell_for_range_by_specific_text(self, sheet_name, xyxy, input_value, color_name):
		"""
		영역안에 입력받은 글자와 같은것이 있으면 색칠하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (any) 입력값
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_for_range_by_specific_text(sheet_name="", xyxy="", input_value="입력값", color_name="yel70")
			<object_name>.paint_cell_for_range_by_specific_text("", "", "입력값", "yel70")
			<object_name>.paint_cell_for_range_by_specific_text(sheet_name="sht1", xyxy="", input_value="입력값123", color_name="yel70")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_obj.Cells(x, y).Value2
				if input_value in value:
					sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint(color_name)

	def paint_cell_for_range_by_words(self, input_list):
		rgbint = self.color.change_any_color_to_rgbint("yel")
		for x in range(self.x1, self.x2 + 1):
			for y in range(self.y1, self.y2 + 1):
				one_value = self.varx["sheet"].Cells(x, y).Value
				temp_int = 0
				for one_word in input_list:
					if one_word in one_value:
						self.sheet_obj.Cells(x, y).Interior.Color = rgbint
						break

	def paint_cell_for_range_by_words_for_range(self, sheet_name, xyxy, input_list):
		"""
		영역안에 원하는 단어의 리스트안에 있는것 있으면 색칠하는 것

		:param input_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_for_range_by_words(sheet_name="", xyxy="", input_list=[1, "abc", "가나다"])
			<object_name>.paint_cell_for_range_by_words("", "", [1, "abc", "가나다"])
			<object_name>.paint_cell_for_range_by_words("sht1", "", [1, "abc", "가나다"])
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = self.varx["sheet"].Cells(x, y).Value
				temp_int = 0
				for one_word in input_list:
					if one_word in one_value:
						sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint("yel")
						break

	def paint_cell_for_range_by_xcolor(self, sheet_name, xyxy, color_name):
		"""
		셀의 배경색을 color_name형식의 색으로 칠하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_by_xcolor(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.paint_cell_by_xcolor("sht1", [1,1,12,23], "red23")
			<object_name>.paint_cell_by_xcolor("", [3,3,5,7], "gra34")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		rgb_int = self.color.change_xcolor_to_rgbint(color_name)
		range_obj.Interior.Color = rgb_int

	def paint_cell_for_range_for_empty_cell(self, sheet_name, xyxy):
		"""
		영역안의 빈셀의 배경색을 칠하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_for_range_for_empty_cell(sheet_name="", xyxy="")
			<object_name>.paint_cell_for_range_for_empty_cell("sht1", [1,1,3,20])
			<object_name>.paint_cell_for_range_for_empty_cell("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		temp_result = 0

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Value
				if one_value == None:
					sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint(16)
					temp_result = temp_result + 1
		return temp_result

	def paint_cell_for_range_for_max_cell(self, sheet_name, xyxy):
		self.paint_cell_for_range_for_max_value_in_each_xline(sheet_name, xyxy, "yel70")

	def paint_cell_for_range_for_max_value_in_each_xline(self, sheet_name, xyxy, color_name):
		"""
		한줄에서 가장 큰 값에 색칠하는 것
		선택한 영역안의 => 각 x라인별로 최대값에 색칠하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_for_range_for_max_value_in_each_xline(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.paint_cell_for_range_for_max_value_in_each_xline("sht1", [1,1,12,23], "red23")
			<object_name>.paint_cell_for_range_for_max_value_in_each_xline("", [3,3,5,7], "gra34")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		all_data = self.read_value_for_range(sheet_name, [x1, y1, x2, y2])
		if not (x1 == x2 and y1 == y2):
			for line_no in range(len(all_data)):
				line_data = all_data[line_no]
				filteredList = list(filter(lambda x: isinstance(x, int) or isinstance(x, float), line_data))
				if filteredList == []:
					pass
				else:
					max_value = max(filteredList)
					x_location = x1 + line_no
					for no in range(len(line_data)):
						y_location = y1 + no
						if (line_data[no]) == max_value:
							sheet_obj.Cells(x_location, y_location).Interior.Color = self.color.change_any_color_to_rgbint(color_name)
		else:
			print("Please re-check selection area")

	def paint_cell_for_range_for_max_value_in_each_yline(self, sheet_name, xyxy):
		"""
		가로줄이아닌 세로줄에서 제일 큰값에 색칠하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_for_range_for_max_value_in_each_yline(sheet_name="", xyxy="")
			<object_name>.paint_cell_for_range_for_max_value_in_each_yline("sht1", [1,1,3,20])
			<object_name>.paint_cell_for_range_for_max_value_in_each_yline("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		all_data = self.read_value_for_range(sheet_name, [y1, x1, y2, x2])

		if not (y1 == y2 and x1 == x2):
			for line_no in range(len(all_data)):
				line_data = all_data[line_no]
				filteredList = list(filter(lambda x: isinstance(x, int) or isinstance(x, float), line_data))
				if filteredList == []:
					pass
				else:
					max_value = max(filteredList)
					y_location = y1 + line_no
					for no in range(len(line_data)):
						x_location = x1 + no
						if (line_data[no]) == max_value:
							sheet_obj.Cells(y_location, x_location).Interior.Color = self.color.change_any_color_to_rgbint(16)
		else:
			print("Please re-check selection area")

	def paint_cell_for_range_for_min_value_in_each_xline(self, sheet_name, xyxy, color_name):
		"""
		선택한 영역안의 => 각 x라인별로 최소값에 색칠하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_for_range_for_min_value_in_each_xline(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.paint_cell_for_range_for_min_value_in_each_xline("sht1", [1,1,12,23], "red23")
			<object_name>.paint_cell_for_range_for_min_value_in_each_xline("", [3,3,5,7], "gra34")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		all_data = self.read_value_for_range(sheet_name, [x1, y1, x2, y2])
		if not (x1 == x2 and y1 == y2):
			for line_no in range(len(all_data)):
				line_data = all_data[line_no]
				filteredList = list(filter(lambda x: isinstance(x, int) or isinstance(x, float), line_data))
				if filteredList == []:
					pass
				else:
					max_value = min(filteredList)
					x_location = x1 + line_no
					for no in range(len(line_data)):
						y_location = y1 + no
						if (line_data[no]) == max_value:
							sheet_obj.Cells(x_location, y_location).Interior.Color = self.color.change_any_color_to_rgbint(color_name)
		else:
			print("Please re-check selection area")

	def paint_cell_for_range_for_specific_text(self, sheet_name, xyxy, input_list, color_name):
		self.paint_cell_for_range_by_specific_text(sheet_name, xyxy, input_list, color_name)

	def paint_cell_for_range_when_input_words(self, sheet_name, xyxy):
		"""
		선택한 영역의 각셀에 아래의 글자가 모두 들어있는 셀에 초록색으로 배는경색 칠하기
		1. 원하자료를 inputbox를 이용하여,를 사용하여 받는다
		2. split함수를 이용하여 리스트로 만들어
		3. 전부 만족한것을 for문으로 만들어 확인한후 색칠을 한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_when_input_words_are_for_cell_value(sheet_name="", xyxy="")
			<object_name>.paint_cell_when_input_words_are_for_cell_value("sht1", [1,1,3,20])
			<object_name>.paint_cell_when_input_words_are_for_cell_value("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		bbb = self.read_messagebox_value("Please input text : in, to, his, with")
		basic_list = []
		for one_data in bbb.split(","):
			basic_list.append(one_data.strip())
		total_no = len(basic_list)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = str(self.read_cell_value(sheet_name, [x, y]))
				temp_int = 0
				for one_word in basic_list:
					if re.match('(.*)' + one_word + '(.*)', one_value):
						temp_int = temp_int + 1
				if temp_int == total_no:
					self.draw_cell_color(sheet_name, [x, y], 4)

	def paint_cell_for_sheet_tab(self, sheet_name, color_name):
		"""
		시트탭의 색을 넣는것
		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_for_sheet_tab(sheet_name="",color_name="yel70")
			<object_name>.paint_cell_for_sheet_tab("", "yel70")
			<object_name>.paint_cell_for_sheet_tab(sheet_name="sht1", color_name="yel70")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.Tab.Color = self.color.change_xcolor_to_rgbint(color_name)

	def paint_color_for_differ_value_in_two_xyxy(self, input_l2d_1, input_l2d_2, colored_tf=False):
		"""
		두개의 리스트가 다른 부분을 찾는데, 기준은 앞의것을 기준으로 한다

		:param input_l2d_1: (list) 2차원의 list형 자료
		:param input_l2d_2: (list) 2차원의 list형 자료
		:param colored_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_color_for_differ_value_in_two_xyxy(input_l2d_1=[[1,1,3,7], [2,2,4,5]],input_l2d_2=[[11,11,13,17], [12,12,14,15]], colored_tf=False)
			<object_name>.paint_color_for_differ_value_in_two_xyxy([[1,1,3,7], [2,2,4,5]], [[11,11,13,17], [12,12,14,15]],  colored_tf=False)
			<object_name>.paint_color_for_differ_value_in_two_xyxy([[1,1,3,7], [2,2,4,5]],[[11,11,13,17], [12,12,14,15]], False)
		"""
		sheet_obj = self.check_sheet_name("")
		result = []
		for l1d, ix in enumerate(input_l2d_1):
			for one_data, iy in enumerate(l1d):
				if input_l2d_1[ix][iy] == input_l2d_2[ix][iy]:
					pass
				else:
					result.append([ix + 1, iy + 1])
					if colored_tf:
						sheet_obj.Cells(ix + 1, iy + 1).Interior.Color = self.color.change_any_color_to_rgbint("red++")

	def paint_data_bar(self, color_name):
		rgbint = self.color.change_any_color_to_rgbint(color_name)
		self.range_obj.FormatConditions.Delete()  # 영역에 포함된 조건부 서식을 지우는 것

		my_bar = self.range_obj.FormatConditions.AddDatabar()
		my_bar.BarFillType = 1  # xlDataBarSolid
		my_bar.BarBorder.Type = 0  # xlDataBarBorderSolid
		my_bar.BarColor.Color = self.color.change_xcolor_to_rgbint(color_name)
		my_bar.BarBorder.Color.TintAndShade = 0

	def paint_data_bar_for_range(self, sheet_name, xyxy, color_name):
		"""
		셀의 입력숫자에 따라서 Data Bar가 타나나도록 만드는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_data_bar_for_range(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.paint_data_bar_for_range("sht1", [1,1,12,23], "red23")
			<object_name>.paint_data_bar_for_range("", [3,3,5,7], "gra34")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.FormatConditions.Delete()  # 영역에 포함된 조건부 서식을 지우는 것

		my_bar = range_obj.FormatConditions.AddDatabar()
		my_bar.BarFillType = 1  # xlDataBarSolid
		my_bar.BarBorder.Type = 0  # xlDataBarBorderSolid
		my_bar.BarColor.Color = self.color.change_xcolor_to_rgbint(color_name)
		my_bar.BarBorder.Color.TintAndShade = 0

	def paint_different_cell_at_2_same_area(self, sheet_name1, xyxy1, sheet_name2, xyxy2):

		self.set_sheet(sheet_name1)
		self.set_range(xyxy1)
		l2d_1 = self.read()
		self.set_sheet(sheet_name2)
		self.set_range(xyxy2)
		l2d_2 = self.read()

		x11, y11, x12, y12 = self.change_any_address_to_xyxy(xyxy1)
		x21, y21, x22, self.y22 = self.change_any_address_to_xyxy(xyxy2)

		for x in range(len(l2d_1)):
			for y in range(len(l2d_1[0])):
				if l2d_1[x][y] != l2d_2[x][y]:
					self.set_sheet(sheet_name1)
					self.set_range([x + x11, y + y11])
					self.paint("yel")
					self.set_sheet(sheet_name2)
					self.set_range([x + x21, y + y21])
					self.paint("yel")

	def paint_different_value_between_2_same_area(self, sheet_name1, xyxy1, sheet_name2, xyxy2, color_name):
		"""
		동일한 사이즈의 2영역의 값을 비교해서, 다른것이 발견되면 색칠하는 것

		:param sheet_name1: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy1: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param sheet_name2: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy2: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56, 색을 나타내는 문자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_different_value_between_2_same_area(sheet_name1="", xyxy1="", sheet_name2="", xyxy2=[1,1,5,12], color_name="yel70")
			<object_name>.paint_different_value_between_2_same_area("sht1", "", "", [1,1,5,12], "yel70")
			<object_name>.paint_different_value_between_2_same_area(sheet_name1="sht2", xyxy1=[1,1,3,5], sheet_name2="", xyxy2=[2,2,5,12], color_name="yel70")
		"""
		l2d_1 = self.read_value_for_range(sheet_name1, xyxy1)
		l2d_2 = self.read_value_for_range(sheet_name2, xyxy2)

		x11, y11, x12, y12 = self.change_any_address_to_xyxy(xyxy1)
		x21, y21, x22, y22 = self.change_any_address_to_xyxy(xyxy2)

		for x in range(len(l2d_1)):
			for y in range(len(l2d_1[0])):
				if l2d_1[x][y] == l2d_2[x][y]:
					pass
				else:
					self.paint_by_any_color_for_range(sheet_name1, [x + x11, y + y11], color_name)
					self.paint_by_any_color_for_range(sheet_name2, [x + x21, y + y21], color_name)

	def paint_empty_cell(self, color_name="yel50"):
		l2d = self.read()
		rgbint = self.color.change_any_color_to_rgbint(color_name)
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			if not l2d[x - self.x1][y - self.y1]:
				self.sheet_obj.Cells(x, y).Interior.Color = rgbint

	def paint_for_differ_value_in_two_range(self, input_l2d_1, input_l2d_2, colored_tf=False):
		"""
		두개의 리스트가 다른 부분을 찾는데, 기준은 앞의것을 기준으로 한다

		:param input_l2d_1: (list) 2차원의 list형 자료
		:param input_l2d_2: (list) 2차원의 list형 자료
		:param colored_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_for_differ_value_in_two_xyxy(input_l2d_1=[[1,1,3,7], [2,2,4,5]],input_l2d_2=[[11,11,13,17], [12,12,14,15]], colored_tf=False)
			<object_name>.paint_for_differ_value_in_two_xyxy([[1,1,3,7], [2,2,4,5]], [[11,11,13,17], [12,12,14,15]],  colored_tf=False)
			<object_name>.paint_for_differ_value_in_two_xyxy([[1,1,3,7], [2,2,4,5]],[[11,11,13,17], [12,12,14,15]], False)
		"""
		sheet_obj = self.check_sheet_name("")
		result = []
		for l1d, ix in enumerate(input_l2d_1):
			for one_data, iy in enumerate(l1d):
				if input_l2d_1[ix][iy] == input_l2d_2[ix][iy]:
					pass
				else:
					result.append([ix + 1, iy + 1])
					if colored_tf:
						sheet_obj.Cells(ix + 1, iy + 1).Interior.Color = self.color.change_any_color_to_rgbint("red++")

	def paint_for_range(self, sheet_name, xyxy, color_name):
		"""
		선택 영역에 색을 칠한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.paint("sht1", [1,1,12,23], "red23")
			<object_name>.paint("", [3,3,5,7], "gra34")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Interior.Color = self.color.change_xcolor_to_rgbint(color_name)

	def paint_for_range_by_rgb(self, sheet_name, xyxy, input_rgb):
		"""
		영역에 색깔을 입힌다 엑셀에서의 색깔의 번호는 아래의 공식처럼 만들어 진다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_range_by_rgb(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.paint_range_by_rgb("", "", "yel70")
			<object_name>.paint_range_by_rgb("sht1", "", "red50")
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		range_obj.Interior.Color = self.change_rgb_to_rgbint(input_rgb)

	def paint_for_range_by_xcolor(self, sheet_name, xyxy, color_name):
		"""
		선택 영역에 색을 칠한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_range_by_xcolor(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.paint_range_by_xcolor("sht1", [1,1,12,23], "red23")
			<object_name>.paint_range_by_xcolor("", [3,3,5,7], "gra34")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Interior.Color = self.color.change_xcolor_to_rgbint(color_name)

	def paint_rgb_set_from_xy_with_new_sheet(self, xy_list, rgb_set):
		"""
		새로운 시트에 rgb set과 cell의 set에 색칠하는것

		:param xy_list: (list) 리스트형식의 셀의 주소가 들어가있는 2차원 리스트형식의 자료, [[1, 1], [2, 3], [2, 4]]
		:param rgb_set: (list) 2차원 리스트형태이며, rgb의 값이 여러개가 들어간 리스트
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_rgb_set_from_xy_with_new_sheet(xy_list=[[1,2], [5,6]], rgb_set=[102, 234, 133])
			<object_name>.paint_rgb_set_from_xy_with_new_sheet([[1,2], [5,6]], [102, 234, 133])
			<object_name>.paint_rgb_set_from_xy_with_new_sheet(xy_list=[[1,12], [5,6]], rgb_set=[102, 234, 133])
		"""
		self.new_sheet()
		sheet_obj = self.check_sheet_name("")
		for ix, one_rgb in rgb_set:
			sheet_obj.Cells(xy_list[0] + ix, xy_list[1]).Interior.Color = self.color.change_rgb_to_rgbint(one_rgb)

	def paint_same_value(self, color_name):
		rgbint = self.color.change_any_color_to_rgbint(color_name)
		set_a = set([])
		for x in range(self.x1, self.x2 + 1):
			for y in range(self.y1, self.y2 + 1):
				value = self.read()
				if value == "" or value == None:
					pass
				else:
					len_old = len(set_a)
					set_a.add(value)
					len_new = len(set_a)
					if len_old == len_new:
						self.sheet_obj.Cells(x, y).Interior.Color = rgbint

	def paint_same_value_as_rgb(self, sheet_name, xyxy):
		"""
		*입력값없이 사용가능*
		선택한 영역에서 2번이상 반복된것만 색칠하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_for_same_value_as_rgb(sheet_name="", xyxy="")
			<object_name>.paint_cell_for_same_value_as_rgb("sht1", [1,1,3,20])
			<object_name>.paint_cell_for_same_value_as_rgb("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		set_a = set([])
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_obj.Cells(x, y).Value
				if value == "" or value == None:
					pass
				else:
					len_old = len(set_a)
					set_a.add(value)
					len_new = len(set_a)
					if len_old == len_new:
						sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint("red++")

	def paint_same_value_by_any_color(self, sheet_name, xyxy, color_name):
		"""
		영역안의 같은 값에 color_name색으로 색칠하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_for_same_value_by_any_color(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.paint_cell_for_same_value_by_any_color("sht1", [1,1,12,23], "red23")
			<object_name>.paint_cell_for_same_value_by_any_color("", [3,3,5,7], "gra34")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		set_a = set([])
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_obj.Cells(x, y).Value
				if value == "" or value == None:
					pass
				else:
					len_old = len(set_a)
					set_a.add(value)
					len_new = len(set_a)
					if len_old == len_new:
						sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint(color_name)

	def paint_same_value_for_range_as_rgb(self, sheet_name, xyxy):
		"""
		*입력값없이 사용가능*
		선택한 영역에서 2번이상 반복된것만 색칠하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_for_range_for_same_value_as_rgb(sheet_name="", xyxy="")
			<object_name>.paint_cell_for_range_for_same_value_as_rgb("sht1", [1,1,3,20])
			<object_name>.paint_cell_for_range_for_same_value_as_rgb("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		set_a = set([])
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = self.read_cell_value(sheet_name, [x, y])
				if value == "" or value == None:
					pass
				else:
					len_old = len(set_a)
					set_a.add(value)
					len_new = len(set_a)
					if len_old == len_new:
						self.draw_cell_color(sheet_name, [x, y], "red++")

	def paint_same_value_for_range_by_56color(self, sheet_name, xyxy, input_56color=12):
		"""
		선택영역 => 같은 값에 색칠

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_56color: 엑셀기본 56색의 번호
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_for_range_for_same_value_by_56color(sheet_name="", xyxy="", input_56color=12)
			<object_name>.paint_cell_for_range_for_same_value_by_56color("", "", 12)
			<object_name>.paint_cell_for_range_for_same_value_by_56color(sheet_name="sht1", xyxy="",  input_56color=12)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		set_a = set([])
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = str(sheet_obj.Cells(x, y).Value2)
				if value == "" or value == None:
					pass
				else:
					len_old = len(set_a)
					set_a.add(value)
					len_new = len(set_a)
					if len_old == len_new:
						sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint(input_56color)

	def paint_same_value_for_range_by_color_name(self, sheet_name, xyxy, color_name):
		"""
		영역안의 같은 값에 color_name색으로 색칠하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_for_range_for_same_value_by_xcolor(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.paint_cell_for_range_for_same_value_by_xcolor("sht1", [1,1,12,23], "red23")
			<object_name>.paint_cell_for_range_for_same_value_by_xcolor("", [3,3,5,7], "gra34")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		set_a = set([])
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = self.read_value_for_cell(sheet_name, [x, y])
				if value == "" or value == None:
					pass
				else:
					len_old = len(set_a)
					set_a.add(value)
					len_new = len(set_a)
					if len_old == len_new:
						sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint(color_name)

	def paint_same_value_for_range_over_n_times(self, sheet_name, xyxy, input_n_times=7):
		"""
		선택한 영역에서 n번이상 반복된 것만 색칠하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_n_times: (int) 정수 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_for_range_for_same_value_over_n_times(sheet_name="", xyxy="", input_n_times=2)
			<object_name>.paint_cell_for_range_for_same_value_over_n_times("", [1,1,3,20], 5)
			<object_name>.paint_cell_for_range_for_same_value_over_n_times("sht1", [1,1,1,20], 4)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		py_dic = {}
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = self.read_value_for_cell(sheet_name, [x, y])
				if one_value != "" and one_value != None:
					if not py_dic[one_value]:
						py_dic[one_value] = 1
					else:
						py_dic[one_value] = py_dic[one_value] + 1

					if py_dic[one_value] >= input_n_times:
						sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint("pin")

	def paint_same_value_for_right_in_2_yline(self, color_name):
		l2d = self.read()
		l1d = self.util.change_l2d_to_l1d(l2d)
		for x in range(self.x1, self.x2 + 1):
			one_value = self.sheet_obj.Cells(x, self.y1 + 1).Value
			if one_value in l1d:
				self.paint(color_name)

	def paint_same_value_for_right_in_2_yline_for_range(self, sheet_name, xyxy, color_name):
		"""
		2열중에서 왼쪽을 기준으로 오른쪽의 값중에서 같은것에 색칠하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_same_value_for_right_in_2_yline(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.paint_same_value_for_right_in_2_yline("sht1", [1,1,12,23], "red23")
			<object_name>.paint_same_value_for_right_in_2_yline("", [3,3,5,7], "gra34")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		l2d = self.read_value_for_range(sheet_name, [x1, y1, x2, y1])
		l1d = self.util.change_l2d_to_l1d(l2d)
		for x in range(x1, x2 + 1):
			one_value = sheet_obj.Cells(x, y1 + 1).Value
			if one_value in l1d:
				self.paint_by_any_color_for_range(sheet_name, xyxy, color_name)

	def paint_same_value_over_n_times(self, input_n_times=7):
		rgbint = self.color.change_any_color_to_rgbint("pin")
		py_dic = {}
		for x in range(self.x1, self.x2 + 1):
			for y in range(self.y1, self.y2 + 1):
				one_value = self.read()
				if one_value != "" and one_value != None:
					if not py_dic[one_value]:
						py_dic[one_value] = 1
					else:
						py_dic[one_value] = py_dic[one_value] + 1

					if py_dic[one_value] >= input_n_times:
						self.sheet_obj.Cells(x, y).Interior.Color = rgbint

	def paint_same_value_over_n_times_for_range(self, sheet_name, xyxy, input_n_times=7):
		"""
		선택한 영역에서 n번이상 반복된 것만 색칠하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_n_times: (int) 정수 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_for_same_value_over_n_times(sheet_name="", xyxy="", input_n_times=2)
			<object_name>.paint_cell_for_same_value_over_n_times("", [1,1,3,20], 5)
			<object_name>.paint_cell_for_same_value_over_n_times("sht1", [1,1,1,20], 4)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		py_dic = {}
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Value
				if one_value:
					if not one_value in  py_dic.keys():
						py_dic[one_value] = 1
					else:
						py_dic[one_value] = py_dic[one_value] + 1

					if py_dic[one_value] >= input_n_times:
						sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint("pin")

	def paint_same_value_with_input_value(self, sheet_name, xyxy, input_value, color_name):
		"""
		영역안에 입력받은 글자와 같은것이 있으면 색칠하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (any) 입력값
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_same_with_input_value(sheet_name="", xyxy="", input_value="입력값", color_name="yel70")
			<object_name>.paint_same_with_input_value("", "", "입력값", "yel70")
			<object_name>.paint_same_with_input_value(sheet_name="sht1", xyxy="", input_value="입력값123", color_name="yel70")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_obj.Cells(x, y).Value2
				if input_value in value:
					sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint(color_name)

	def paint_search_for_range_range_by_regex(self, sheet_name, xyxy, input_xre, color_name):
		"""
		엑셀의 영역에서 값을 찾으면, 셀에 색칠하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_xre: (str) xre형식의 문자열
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_search_range_by_regex(sheet_name="", xyxy="", input_xre="[영어:1~4][한글:3~10]", color_name="yel70")
			<object_name>.paint_search_range_by_regex("sht1", "", "[영어:1~4][한글:3~10]", color_name="yel70")
			<object_name>.paint_search_range_by_regex(sheet_name="", xyxy=[1,1,5,7], input_xre="[시작:처음][영어:1~4][한글:3~10]", color_name="yel70")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		l2d = range_obj.Formula
		for ix, l1d in enumerate(l2d):
			for iy, value in enumerate(l1d):
				if not value or str(value).startswith("="):
					pass
				else:
					temp = self.rex.search_all_by_xsql(input_xre, value)
				if temp:
					sheet_obj.Cells(x1 + ix, y1 + iy).Interior.Color = self.color.change_any_color_to_rgbint(color_name)

	def paint_search_range_by_regex(self, input_xre, color_name):
		rgbint = self.color.change_any_color_to_rgbint(color_name)
		l2d = self.range_obj.Formula
		for ix, l1d in enumerate(l2d):
			for iy, value in enumerate(l1d):
				if not value or str(value).startswith("="):
					pass
				else:
					temp = self.rex.search_all_by_xsql(input_xre, value)
				if temp:
					self.sheet_obj.Cells(self.x1 + ix,
										 self.y1 + iy).Interior.Color = rgbint

	def paint_selection(self, color_name):
		self.range_obj.Interior.Color = self.color.change_xcolor_to_rgbint(color_name)

	def paint_selection_by_xcolor(self, color_name):
		"""
		선택 영역의 배경색을 칠하는것
		색을 나타내는 형식은 xcolor형식으로 입력함

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_selection_by_xcolor(color_name="yel70")
			<object_name>.paint_selection_by_xcolor("yel70")
			<object_name>.paint_selection_by_xcolor("red50")
		"""
		sheet_obj = self.check_sheet_name("")
		x1, y1, x2, y2 = self.change_any_address_to_xyxy("")
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		range_obj.Interior.Color = self.color.change_xcolor_to_rgbint(color_name)

	def paint_sheet_tab(self, color_name):
		self.sheet_obj.Tab.Color = self.color.change_xcolor_to_rgbint(color_name)

	def paint_sheet_tab_by_xcolor(self, sheet_name, color_name):
		"""
		시트탭의 색을 넣는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_sheet_tab_by_xcolor(sheet_name="", color_name="yel70")
			<object_name>.paint_sheet_tab_by_xcolor("", "yel70")
			<object_name>.paint_sheet_tab_by_xcolor("sht1", "red50")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.Tab.Color = self.color.change_xcolor_to_rgbint(color_name)

	def paint_space_cell_for_range_by_any_color(self, sheet_name, xyxy, color_name):
		"""
		영역안의 셀의 배경색을 color_name색으로 정하는 것
				빈셀처럼 보이는데 space문자가 들어가 있는것 찾기
		선택한 영역의 셀을 하나씩 읽어와서 re모듈을 이용해서 공백만 있는지 확인한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_cell_for_space_cell_by_any_color(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.paint_cell_for_space_cell_by_any_color("sht1", [1,1,12,23], "red23")
			<object_name>.paint_cell_for_space_cell_by_any_color("", [3,3,5,7], "gra34")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Value
				com = re.compile(r"^\s+")
				if one_value != None:
					if com.search(one_value):
						sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint(color_name)

	def paint_specific_text(self, sheet_name, xyxy, input_value, color_name):
		"""
		영역안에 입력받은 글자와 같은것이 있으면 색칠하는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (any) 입력값
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_specific_text(sheet_name="", xyxy="", input_value="입력값", color_name="yel70")
			<object_name>.paint_specific_text("", "", "입력값", "yel70")
			<object_name>.paint_specific_text(sheet_name="sht1", xyxy="", input_value="입력값123", color_name="yel70")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_obj.Cells(x, y).Value2
				if isinstance(value, str) and input_value in value:
					sheet_obj.Cells(x, y).Interior.Color = self.color.change_any_color_to_rgbint(color_name)

	def paint_start_cell_of_same_value_as_yline(self, color_name):
		rgbint = self.color.change_any_color_to_rgbint(color_name)
		found = False
		gijun_no = 0
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			value = self.sheet_obj.Cells(x, y).Value
			value2 = self.sheet_obj.Cells(x + 1, y).Value
			if value == value2 and value2 != None and value2 != "":
				if not found:
					gijun_no = x
					found = True
			else:
				if found:
					self.sheet_obj.Cells(gijun_no, y).Interior.Color = rgbint
					found = False
				gijun_no = x

	def paint_start_cell_of_same_value_as_yline_for_range(self, sheet_name, xyxy, color_name):
		"""
		세로로 같은값이 연속되는 셀의 시작 셀에 색칠하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_start_cell_of_same_value_as_yline_for_range(sheet_name="", xyxy="", color_name="yel70")
			<object_name>.paint_start_cell_of_same_value_as_yline_for_range("sht1", [1,1,12,23], "red23")
			<object_name>.paint_start_cell_of_same_value_as_yline_for_range("", [3,3,5,7], "gra34")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		xyxy = self.change_any_address_to_xyxy(xyxy)
		gigun_value = ""
		found = False
		gijun_no = 0
		for y in range(xyxy[1], xyxy[3] + 1):
			for x in range(xyxy[0], xyxy[2] + 1):
				value = sheet_obj.Cells(x, y).Value
				value2 = sheet_obj.Cells(x + 1, y).Value
				if value == value2 and value2 != None and value2 != "":
					if not found:
						gijun_no = x
						found = True
				else:
					if found:
						sheet_obj.Cells(gijun_no, y).Interior.Color = self.color.change_any_color_to_rgbint(color_name)
						found = False
					gijun_no = x
					gijun_value = value

	def paint_words(self, input_list):
		"""
		선택영역안의 값중에 입력값중 하나가 잇으면, 셀의 배경색을 칠하기

		:param input_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paint_words(input_list=[1, "abc", "가나다"])
			<object_name>.paint_words([1, "abc", "가나다"])
			<object_name>.paint_words([1, "abc", "가나다"])
		"""
		bbb = input_list
		basic_list = [one_data.strip() for one_data in bbb.split(",")]
		total_no = len(basic_list)
		for x in range(self.varx["x1"], self.varx["x2"] + 1):
			for y in range(self.varx["y1"], self.varx["y2"] + 1):
				one_value = self.varx["sheet"].Cells(x, y).Value
				temp_int = 0
				for one_word in basic_list:
					if re.match('(.*)' + one_word + '(.*)', one_value):
						temp_int = temp_int + 1
				if temp_int == total_no:
					# pcell_dot.sheet_obj.range().paint([x, y], 4)
					pass

	def password_for_sheet(self, sheet_name, password="1234"):
		"""
		시트를 암호로 저장

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param password: (str) 암호
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_password_for_sheet(sheet_name="", password="1234")
			<object_name>.set_password_for_sheet("", "abc1234")
			<object_name>.set_password_for_sheet(sheet_name="sht1", password="1234")
		"""
		self.set_sheet_lock(sheet_name, password)

	def paste_format_only(self):
		self.range_obj.PasteSpecial(Paste=-4122)  # Paste=win32.constants.xlPasteFormats)

	def paste_format_only_for_range(self, sheet_name, xyxy):
		"""
		서식만 붙여넣기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paste_format_only_for_range(sheet_name="", xyxy="")
			<object_name>.paste_format_only_for_range("sht1", [1,1,3,20])
			<object_name>.paste_format_only_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.PasteSpecial(Paste=-4122)  # Paste=win32.constants.xlPasteFormats)

	def paste_range(self):
		self.select_sheet()
		self.sheet_obj.Cells(self.x1, self.y1).Select()
		self.sheet_obj.Paste()

	def paste_range_for_sheet(self, sheet_name, xyxy):
		"""
		복사한것을 붙여넣기 하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.paste_range(sheet_name="", xyxy="")
			<object_name>.paste_range("sht1", [1,1,3,20])
			<object_name>.paste_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		self.select_sheet(sheet_name)
		sheet_obj.Cells(x1, y1).Select()
		sheet_obj.Paste()

	def pattern_for_range(self, sheet_name, xyxy, input_list=[]):
		"""
		셀에 색상과 특정한 패턴을 집어 넣어서 다른것들과 구분할수가 있다

		1. 배경색에 격자무늬를 집어넣을수가 있는데, 이것은 패턴을 칠하고 남은 공간을 칠할수가 있다
		2. 배경색 + 무늬선택(색과 무늬형식)
		3. 만약 배경색으로 채우기효과를 주면서 그라데이션을 준다면, 무늬선택은 불가능하다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_pattern_for_range(sheet_name="", xyxy="", input_list=[1, "abc", "가나다"])
			<object_name>.set_pattern_for_range("", "", [1, "abc", "가나다"])
			<object_name>.set_pattern_for_range(sheet_name="sht1", xyxy=[1,1,7,10], input_list=[1, "abc", "가나다"])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		input_list = self.check_input_data(input_list)

		self.setup_basic_data(sheet_name, xyxy)
		if input_list:
			# 아무것도 없으면, 기존의 값을 사용하고, 있으면 새로이 만든다
			if isinstance(input_list, list):
				self.setup_font(input_list)
			elif isinstance(input_list, dict):
				# 만약 사전 형식이면, 기존에 저장된 자료로 생각하고 update한다
				self.varx["pattern"].update(input_list)
		a = 2
		if a == 1:
			range_obj.Interior.Color = 5296274
			range_obj.Interior.Pattern = self.varx["range_color"]["pattern"]
			range_obj.Interior.PatternColor = self.varx["range_color"]["pattern"]

		elif a == 2:
			range_obj.Interior.Gradient.Degree = 180
			range_obj.Interior.Gradient.ColorStops.Clear()
			range_obj.Interior.Gradient.ColorStops.Add(0)

		elif a == 3:
			range_obj.Interior.Color = 5296274
			range_obj.Interior.Pattern = self.varx["range_color"]["pattern"]  # xlSolid
			range_obj.Interior.PatternColor = self.varx["range_color"]["pattern"]  # PatternColorIndex = xlAutomatic
			range_obj.Interior.ThemeColor = 4  # xlThemeColorDark1 색상과 색조를 미리 설정한것을 불러다가 사용하는것
			# 이것은 기본적으로 마우스의 색을 선택할때 나타나는 테마색을 말하는 것이다

			range_obj.Interior.TintAndShade = -0.249977111117893  # 명암을 조절
			range_obj.Interior.PatternTintAndShade = 0

		return self.varx["range_color"]

	def pen_color_style_thickness(self, color_name="yel70", style="", thickness=5):
		"""
		여러곳에 사용하기위해 공통변수에 색, 모양, 두께를 설정하는 것

		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:param style: (str) 입력으로 들어오는 텍스트, 모양을 나타내는 스타일을 넣는 것
		:param thickness: (int) 선의 두께
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_pen_color_style_thickness_for_obj(color_name="yel70", style=4, thickness=5)
			<object_name>.set_pen_color_style_thickness_for_obj(color_name="red45", style=3, thickness=4)
			<object_name>.set_pen_color_style_thickness_for_obj(color_name="yel70", style=2, thickness=3)
		"""

		self.varx["pen_color"] = self.color.change_xcolor_to_rgbint(color_name)
		self.varx["pen_style"] = style
		self.varx["pen_thickness"] = thickness

	def pen_color_style_thickness_for_obj(self, input_shape_obj="", color_name="yel70", style=4, thickness=5):
		"""
		도형객체의 색, 모양, 두께를 설정하는 것

		:param input_shape_obj: (object) 객체, 도형객체
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:param style: (str) 입력으로 들어오는 텍스트, 모양을 나타내는 스타일을 넣는 것
		:param thickness: (int) 선의 두께
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_pen_color_style_thickness_for_obj(input_shape_obj=shape_obj1, color_name="yel70", style=4, thickness=5)
			<object_name>.set_pen_color_style_thickness_for_obj(input_shape_obj=shape_obj2, color_name="red45", style=3, thickness=4)
			<object_name>.set_pen_color_style_thickness_for_obj(input_shape_obj=shape_obj3, color_name="yel70", style=2, thickness=3)
		"""
		input_shape_obj.DashStyle = style
		input_shape_obj.ForeColor.RGB = self.color.change_xcolor_to_rgbint(color_name)
		input_shape_obj.Weight = thickness

	def pen_start_style(self, length=2, style=1, width_float=2):
		"""
		도형객체에 모두 사용하기위해 시작모양을 설정하는 것

		:param length: (int) 길이를 나타내는 정수
		:param style: (str) 입력으로 들어오는 텍스트, 모양을 나타내는 스타일을 넣는 것
		:param width_float: (int) 넓이를 나타내는 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_pen_start_style(length=2, style=1, width_float=2)
			<object_name>.set_pen_start_style(3, 1, 2)
			<object_name>.set_pen_start_style(length=7, style=2, width_float=2)
		"""
		self.varx["start_point_length"] = length  # 2-default, 3-long, 1-short
		self.varx["start_point_style"] = style  # 1-없음,2-삼각형,3-얇은화살촉,4-화살촉,5-다이아몬드,6-둥근
		self.varx["start_point_width"] = width_float  # 2-default, 3-넓은, 1-좁은

	def pen_start_style_for_obj(self, input_shape_obj="", length=2, style=1, width_float=2):
		"""
		도형객체의 시작모양을 설정하는 것

		:param input_shape_obj: (object) 객체, 도형객체
		:param length: (int) 길이를 나타내는 정수
		:param style: (str) 입력으로 들어오는 텍스트, 모양을 나타내는 스타일을 넣는 것
		:param width_float: (int) 넓이를 나타내는 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_pen_start_style_for_obj(input_shape_obj=shape_obj1, length=2, style=1, width_float=2)
			<object_name>.set_pen_start_style_for_obj(shape_obj2, 3, 1, 2)
			<object_name>.set_pen_start_style_for_obj(input_shape_obj=shape_obj3, length=7, style=2, width_float=2)
		"""
		input_shape_obj.BeginArrowheadlength = length  # 2-default, 3-long, 1-short
		input_shape_obj.BeginArrowheadstyle = style  # 1-없음,2-삼각형,3-얇은화살촉,4-화살촉,5-다이아몬드,6-둥근
		input_shape_obj.BeginArrowheadwidth = width_float  # 2-default, 3-넓은, 1-좁은

	def pick_ylines_at_l2d(self, input_l2d, input_l1d):
		"""
		2차원자료중에서 원하는 가로열들의 자료만 갖고오는 것

		:param input_l2d: (list) 2차원의 list형 자료
		:param input_l1d: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.pick_ylines_at_l2d(input_l2d=[[1, 2], [4, 5]], input_l1d=[1, "abc", "가나다"])
			<object_name>.pick_ylines_at_l2d([[1, 2], [4, 5]], [1, "abc", "가나다"])
			<object_name>.pick_ylines_at_l2d(input_l2d=[[1,2,3], [4,5,6],[27,28,39]], input_l1d=[23,"abc","가나다"])
		"""
		input_l2d = self.check_input_data(input_l2d)
		result = []
		for one_list in input_l2d:
			temp = [one_list[index] for index in input_l1d]
			result.append(temp)
		return result

	def ppt_make_ppt_table_from_xl_data(self):
		"""
		엑셀의 테이블 자료가 잘 복사가 않되는것 같아서, 아예 하나를 만들어 보았다
		엑셀의 선택한 영역의 테이블 자료를 자동으로 파워포인트의 테이블 형식으로 만드는 것이다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.ppt_make_ppt_table_from_xl_data()
		"""

		activesheet_name = self.get_activesheet_name()
		[x1, y1, x2, y2] = self.read_select_address()

		Application = win32com.client.Dispatch("Powerpoint.Application")
		Application.Visible = True
		active_ppt = Application.Activepresentation
		slide_no = active_ppt.Slides.Count + 1

		new_slide = active_ppt.Slides.Add(slide_no, 12)
		new_table = active_ppt.Slides(slide_no).Shapes.AddTable(x2 - x1 + 1, y2 - y1 + 1)
		shape_no = active_ppt.Slides(slide_no).Shapes.Count

		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				value = self.read_value_for_cell(activesheet_name, [x, y])
				active_ppt.Slides(slide_no).Shapes(shape_no).Table.Cell(x - x1 + 1,
																			  y - y1 + 1).Shape.TextFrame.TextRange.Text = value

	def preview(self):
		self.sheet_obj.PrintPreview()

	def preview_for_sheet(self, sheet_name):
		"""
		입력으로 들어온 시트를 미리보기기능입니다
		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.preview(sheet_name="")
			<object_name>.preview("sht1")
			<object_name>.preview("")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.PrintPreview()

	def print_area(self, fit_wide):

		new_xyxy = self.xyxy2_to_r1c1('')
		self.sheet_obj.PageSetup.PrintArea = new_xyxy

		self.sheet_obj.PageSetup.Orientation = 1
		self.sheet_obj.PageSetup.Zoom = False
		self.sheet_obj.PageSetup.FitToPagesTall = False
		self.sheet_obj.PageSetup.FitToPagesWide = fit_wide

	def print_area_for_sheet(self, sheet_name, xyxy, fit_wide=1):
		"""
		프린트영역을 설정

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param fit_wide: (int) 넓이를 용지에 맞게 넓힐것인지를 설정하는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_print_area(sheet_name="", xyxy="", fit_wide=1)
			<object_name>.set_print_area("", "", 1)
			<object_name>.set_print_area(sheet_name="sht1", xyxy=[1,1,7,10], fit_wide=1)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		new_xyxy = self.xyxy2_to_r1c1(xyxy)
		sheet_obj.PageSetup.PrintArea = new_xyxy

		sheet_obj.PageSetup.Orientation = 1
		sheet_obj.PageSetup.Zoom = False
		sheet_obj.PageSetup.FitToPagesTall = False
		sheet_obj.PageSetup.FitToPagesWide = fit_wide

	def print_as_pdf(self, xyxy, filename, ):
		self.sheet_obj.ExportAsFixedFormat(0, filename)

	def print_as_pdf_for_range(self, sheet_name, xyxy, filename):
		"""
		sheet_obj.PageSetup.Zoom = False
		sheet_obj.PageSetup.FitToPagesTall = 1
		sheet_obj.PageSetup.FitToPagesWide = 1
		sheet_obj.PageSetup.LeftMargin = 25
		sheet_obj.PageSetup.RightMargin = 25
		sheet_obj.PageSetup.TopMargin = 50
		sheet_obj.PageSetup.BottomMargin = 50
		sheet_obj.ExportAsFixedFormat(0, filename)
		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param filename: (str) 화일의 이름을 나타내는 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.print_as_pdf(sheet_name="", xyxy="", input_full_path="D:\\my_folder" )
			<object_name>.print_as_pdf(sheet_name="sht1", xyxy=[1,1,4,7], input_full_path="D:\\my_folder1" )
			<object_name>.print_as_pdf(sheet_name="", xyxy="", input_full_path="D:\\my_folder2")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.ExportAsFixedFormat(0, filename)

	def print_header(self, position, input_value=""):

		temp_dic = {"화일명": "&F", "시간": "&T", "경로": "&Z", "현재페이지": "&N", "총페이지": "&P", "날짜": "&D"}
		for one in temp_dic.keys():
			input_value = input_value.replace(one, temp_dic[one])

		if position == "left":
			self.sheet_obj.PageSetup.LeftHeader = input_value
		elif position == "center":
			self.sheet_obj.PageSetup.CenterHeader = input_value
		elif position == "right":
			self.sheet_obj.PageSetup.RightHeader = input_value

	def print_header_for_sheet(self, sheet_name, position, input_value):
		"""
		입력한 값들을 엑셀에서 사용하는 형식으로 변경하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param position: (str) 입력으로 들어오는 텍스트, 위치를 나타내는 문자 (str) 위치를 나타내는 문자
		:param input_value: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_print_header(sheet_name="", position=3, input_value="입력값1")
			<object_name>.set_print_header("", 3, "입력값1")
			<object_name>.set_print_header(sheet_name="sht1", position=7, input_value="입력값1")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		temp_dic = {"화일명": "&F", "시간": "&T", "경로": "&Z", "현재페이지": "&N", "총페이지": "&P", "날짜": "&D"}
		for one in temp_dic.keys():
			input_value = input_value.replace(one, temp_dic[one])

		if position == "left":
			sheet_obj.PageSetup.LeftHeader = input_value
		elif position == "center":
			sheet_obj.PageSetup.CenterHeader = input_value
		elif position == "right":
			sheet_obj.PageSetup.RightHeader = input_value

	def print_label_style(self, input_l2d, line_list, start_xy, size_xy, y_line, position):
		input_l2d = self.check_input_data(input_l2d)
		line_list = self.check_input_data(line_list)

		changed_input_l2d = self.pick_ylines_at_l2d(input_l2d, line_list)
		for index, l1d in enumerate(changed_input_l2d):
			new_start_x, new_start_y = self.util.new_xy(index, start_xy, size_xy, y_line)
			for index_2, one_value in enumerate(l1d):
				self.sheet_obj.Cells(new_start_x + position[index_2][0], new_start_y + position[index_2][1]).Value = \
					l1d[index_2]

	def print_label_style_for_sheet(self, sheet_name, input_l2d, line_list, start_xy, size_xy, y_line, position):
		"""
		라벨프린트식으로 만드는 것
		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_l2d: (list) 2차원의 list형 자료
		:param line_list: (list) 라인의 번호를 나타내는 숫자형 리스트
		:param start_xy: (list or str) 셀영역으로 [1,2], ''(현재 선택 영역)로 사용가능
		:param size_xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param y_line: (int) 1부터 시작하는 세로를 나타내는 column의 숫자
		:param position: (str) 입력으로 들어오는 텍스트, 위치를 나타내는 문자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.print_label_style(sheet_name="", input_l2d=[[1, 2], [4, 5]], line_list=[1, 3, 5], start_xy=[1,1], size_xy=[2, 4], y_line=2, position=3)
			<object_name>.print_label_style("", [[1, 2], [4, 5]], [1, 3, 5], [1,1], [2, 4], 2, 3)
			<object_name>.print_label_style(sheet_name="sht1", input_l2d=[[1, 2], [4, 5]], line_list=[2,3,5], start_xy=[1,1], size_xy=[2, 4], y_line=4, position=7)
		"""
		sheet_obj = self.check_sheet_name("")
		input_l2d = self.check_input_data(input_l2d)
		line_list = self.check_input_data(line_list)

		changed_input_l2d = self.pick_ylines_at_l2d(input_l2d, line_list)
		for index, l1d in enumerate(changed_input_l2d):
			new_start_x, new_start_y = self.util.new_xy(index, start_xy, size_xy, y_line)
			for index_2, one_value in enumerate(l1d):
				sheet_obj.Cells(new_start_x + position[index_2][0], new_start_y + position[index_2][1]).Value = l1d[index_2]

	def print_letter_cover(self):
		"""
		봉투인쇄

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.print_letter_cover()
		"""
		# 기본적인 자료 설정
		sheet_obj = self.check_sheet_name("")
		data_from = [["sheet1", [1, 2]], ["sheet1", [1, 4]], ["sheet1", [1, 6]], ["sheet1", [1, 8]]]
		data_to = [["sheet2", [1, 2]], ["sheet2", [2, 2]], ["sheet2", [3, 2]], ["sheet2", [2, 3]]]
		no_start = 1
		no_end = 200
		step = 5
		# 실행되는 구간
		for no in range(no_start, no_end):
			for one in range(len(data_from)):
				value = self.read_value_for_cell(data_from[one][0], data_from[one][1])
				sheet_obj.Cells(data_to[one][1][0] + (step * no), data_to[one][1][1]).Value = value

	def print_page(self, input_dic):
		self.sheet_obj.PageSetup.Zoom = False
		self.sheet_obj.PageSetup.FitToPagesTall = 1
		self.sheet_obj.PageSetup.FitToPagesWide = 1
		# self.sheet_obj.PageSetup.PrintArea = print_area
		self.sheet_obj.PageSetup.LeftMargin = 25
		self.sheet_obj.PageSetup.RightMargin = 25
		self.sheet_obj.PageSetup.TopMargin = 50
		self.sheet_obj.PageSetup.BottomMargin = 50
		# self.sheet_obj.ExportAsFixedFormat(0, path_to_pdf)
		self.sheet_obj.PageSetup.LeftFooter = "&D"  # 날짜
		self.sheet_obj.PageSetup.LeftHeader = "&T"  # 시간
		self.sheet_obj.PageSetup.CenterHeader = "&F"  # 화일명
		self.sheet_obj.PageSetup.CenterFooter = "&N/&P"  # 현 page/ 총 page
		self.sheet_obj.PageSetup.RightHeader = "&Z"  # 화일 경로
		self.sheet_obj.PageSetup.RightFooter = "&P+33"  # 현재 페이지 + 33

	def print_page_for_sheet(self, sheet_name, input_dic):
		"""
		좀더 사용하기 쉽도록 변경이 필요

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_dic: (dic) 사전형으로 입력되는 자료 사전형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_print_page(sheet_name="", input_dic = {"key1":1, "line_1":"red", "input_color":"red", "font_bold":1})
			<object_name>.set_print_page("", {"key1":1, "line_1":"red", "input_color":"red", "font_bold":1})
			<object_name>.set_print_page(sheet_name="sht1", input_dic = {"key1":1, "line_2":"red", "input_color1":"red", "font_bold1":1}])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.PageSetup.Zoom = False
		sheet_obj.PageSetup.FitToPagesTall = 1
		sheet_obj.PageSetup.FitToPagesWide = 1
		# sheet_obj.PageSetup.PrintArea = print_area
		sheet_obj.PageSetup.LeftMargin = 25
		sheet_obj.PageSetup.RightMargin = 25
		sheet_obj.PageSetup.TopMargin = 50
		sheet_obj.PageSetup.BottomMargin = 50
		# sheet_obj.ExportAsFixedFormat(0, path_to_pdf)
		sheet_obj.PageSetup.LeftFooter = "&D"  # 날짜
		sheet_obj.PageSetup.LeftHeader = "&T"  # 시간
		sheet_obj.PageSetup.CenterHeader = "&F"  # 화일명
		sheet_obj.PageSetup.CenterFooter = "&N/&P"  # 현 page/ 총 page
		sheet_obj.PageSetup.RightHeader = "&Z"  # 화일 경로
		sheet_obj.PageSetup.RightFooter = "&P+33"  # 현재 페이지 + 33

	def print_preview(self):
		self.sheet_obj.PrintPreview()

	def print_preview_for_sheet(self, sheet_name):
		"""
		미리보기기능입니다
		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.print_preview_for_sheet(sheet_name="")
			<object_name>.print_preview_for_sheet("sht1")
			<object_name>.print_preview_for_sheet("")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.PrintPreview()

	def quit(self):
		"""
		엑셀 프로그램을 끄는것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.quit()
		"""
		self.xlapp.Quit()

	def range_name_for_range(self, sheet_name, xyxy, input_name):
		"""
		영역에 이름을 설정하는 것입니다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_name: (str) 입력으로 들어오는 텍스트, 설정할 이름으로 사용할 문자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_range_name_for_range(sheet_name="", xyxy="", input_name="rng_name1")
			<object_name>.set_range_name_for_range("", "rng_name1")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		self.xlbook.Names.Add(input_name, range_obj)

	def read(self):
		result = self.util.change_any_type_to_l2d(self.range_obj.Value)
		result = self.check_input_data(result)
		return result

	def read_activecell(self):
		return self.xlapp.ActiveCell.Value2

	def read_activecell_n_yno(self, input_yno):
		"""
		현재 선택된 셀의 x번호와 입력받은 y줄의 번호를 조합한 셀의 값을 읽어오는것

		:param input_yno: (int) 정수, 엑셀의 세로열(column) 번호를 나타내는것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_activecell_n_yno(3)
		"""
		xyxy = self.get_address_for_activecell()
		value = self.read_value_for_cell("", [xyxy[0], input_yno])
		return value

	def read_address_for_selection(self):
		"""
		선택된 영역의 주소값을 갖고온다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.get_address_for_selection()
		"""
		result = ""
		temp_address = self.xlapp.Selection.Address
		temp_list = temp_address.split(",")
		if len(temp_list) == 1:
			result = self.change_any_address_to_xyxy(temp_address)
		if len(temp_list) > 1:
			result = []
			for one_address in temp_list:
				result.append(self.change_any_address_to_xyxy(one_address))
		return result

	def read_as_dic_with_xy_position(self):
		result = {}
		l2d = self.read()

		for ix, l1d in enumerate(l2d):
			for iy, one_value in enumerate(l1d):
				if one_value in result.keys():
					result[ix + 1, iy + 1].append([one_value])
				else:
					result[one_value] = [[ix + 1, iy + 1]]
		result = self.check_input_data(result)
		return result

	def read_as_dic_with_xy_position_for_range(self, sheet_name, xyxy):
		"""
		선택된 영역안의 2차원자료를 사전형식으로 돌려 주는 것
		같은값을 발견하면, 주소를 추가하는 형태
		예: [["가나","다라"],["ab", "다라"]] => {"가나":[[1,1]], "다라":[[1,2], [2,2]],"ab":[[2,1]]}

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_as_dic_with_xy_position(sheet_name="", xyxy="")
			<object_name>.read_as_dic_with_xy_position("sht1", [1,1,3,20])
			<object_name>.read_as_dic_with_xy_position("", "")
		"""
		result = {}
		l2d = self.read_value_for_range(sheet_name, xyxy)

		for ix, l1d in enumerate(l2d):
			for iy, one_value in enumerate(l1d):
				if one_value in result.keys():
					result[ix + 1, iy + 1].append([one_value])
				else:
					result[one_value] = [[ix + 1, iy + 1]]
		result = self.check_input_data(result)
		return result

	def read_as_l1d_for_xline_base(self):
		result = []
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = self.sheet_obj.Cells(x, y).Value
			result.append(one_value)
		result = self.check_input_data(result)
		return result

	def read_as_l1d_for_yline_base(self):
		result = [self.sheet_obj.Cells(x, y).Value for y in range(self.y1, self.y2 + 1) for x in
				  range(self.x1, self.x2 + 1)]

		return result

	def read_as_text(self):
		result = []
		for x in range(self.x1, self.x2 + 1):
			temp = []
			for y in range(self.y1, self.y2 + 1):
				one_value = self.sheet_obj.Cells(x, y).Text
				temp.append(one_value)
			result.append(temp)
		result = self.check_input_data(result)
		return result

	def read_as_text_for_range(self, sheet_name, xyxy):
		"""
		읽어온값 자체를 변경하지 않고 그대로 읽어오는 것 그자체로 text 형태로 돌려주는것 만약 스캔을 한 숫자가 .를 잘못 .으로 읽었다면
		48,100 => 48.1로 엑셀이 바로 인식을 하는데 이럴때 48.100 으로 읽어와서 바꾸는 방법을 하기위해 사용하는 방법

		:param sheet_ name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_as_text(sheet_name="", xyxy="")
			<object_name>.read_as_text("sht1", [1,1,3,20])
			<object_name>.read_as_text("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		result = []
		for x in range(x1, x2 + 1):
			temp = []
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Text
				temp.append(one_value)
			result.append(temp)
		result = self.check_input_data(result)
		return result

	def read_cell(self):
		return self.sheet_obj.Cells(self.x1, self.y1).Value

	def read_check_date(self):
		result = self.check_input_data(self.range_obj.Value)
		return result

	def read_continuous_range(self):
		bottom = self.x1
		while self.sheet_obj.Cells(bottom + 1, self.y1).Value not in [None, '']:
			bottom = bottom + 1
		right = self.y1  # 오른쪽 열
		while self.sheet_obj.Cells(self.x1, right + 1).Value not in [None, '']:
			right = right + 1
		result = self.sheet_obj.Range(self.sheet_obj.Cells(self.x1, self.y1), self.sheet_obj.Cells(bottom, right)).Value

		return result

	def read_continuous_range_for_range(self, sheet_name, xyxy):
		"""
		read_continuousrange_value(sheet_name="", xyxy="")
		현재선택된 셀을 기준으로 연속된 영역을 가지고 오는 것입니다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_continuous_range(sheet_name="", xyxy="")
			<object_name>.read_continuous_range("sht1", [1,1,3,20])
			<object_name>.read_continuous_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		bottom = x1
		while sheet_obj.Cells(bottom + 1, y1).Value not in [None, '']:
			bottom = bottom + 1
		right = y1  # 오른쪽 열
		while sheet_obj.Cells(x1, right + 1).Value not in [None, '']:
			right = right + 1
		result = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(bottom, right)).Value

		return result

	def read_continuous_same_value(self):
		row = self.x1
		col = self.y1
		bottom = row  # 아래의 행을 찾는다
		while self.sheet_obj.Cells(bottom + 1, col).Value not in [None, '']:
			bottom = bottom + 1
		right = col  # 오른쪽 열
		while self.sheet_obj.Cells(row, right + 1).Value not in [None, '']:
			right = right + 1
		result = self.sheet_obj.Range(self.sheet_obj.Cells(row, col), self.sheet_obj.Cells(bottom, right)).Value
		result = self.check_input_data(result)
		return result

	def read_datas_for_cell(self, sheet_name, xy):
		"""
		하나의 셀에 대한 중요한 정보들을 읽어오는 것		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_datas_for_cell(sheet_name="", xy=[7, 7])
			<object_name>.read_datas_for_cell("", [1,1])
			<object_name>.read_datas_for_cell("", [1,20])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		one_cell = sheet_obj.Cells(xy[0], xy[1])
		result = {}
		y = result["x"] = xy[0]
		x = result["y"] = xy[1]
		result["value"] = one_cell.Value
		result["value2"] = one_cell.Value2
		result["formula"] = one_cell.Formula
		result["formular1c1"] = one_cell.FormulaR1C1
		result["text"] = one_cell.Text
		if result["value"] != "" and result["value"] != None:
			# 값이 없으면 font에 대한 것을 읽지 않는다
			result["font_dic"]["background"] = one_cell.Font.Background
			result["font_dic"]["bold"] = one_cell.Font.Bold
			result["font_dic"]["color"] = one_cell.Font.Color
			result["font_dic"]["colorindex"] = one_cell.Font.ColorIndex
			# result["font_dic"]["creator"] = one_cell.Font.Creator
			result["font_dic"]["style"] = one_cell.Font.FontStyle
			result["font_dic"]["italic"] = one_cell.Font.Italic
			result["font_dic"]["name"] = one_cell.Font.Name
			result["font_dic"]["size"] = one_cell.Font.Size
			result["font_dic"]["strikethrough"] = one_cell.Font.Strikethrough
			result["font_dic"]["subscript"] = one_cell.Font.Subscript
			result["font_dic"]["superscript"] = one_cell.Font.Superscript
			# result["font_dic"]["themecolor"] = one_cell.Font.ThemeColor
			# result["font_dic"]["themefont"] = one_cell.Font.ThemeFont
			# result["font_dic"]["tintandshade"] = one_cell.Font.TintAndShade
			result["font_dic"]["underline"] = one_cell.Font.Underline
		try:
			result["memo"] = one_cell.Comment.Text()
		except:
			result["memo"] = ""
		result["background_color"] = one_cell.Interior.Color
		result["background_colorindex"] = one_cell.Interior.ColorIndex
		result["numberformat"] = one_cell.NumberFormat
		if one_cell.Borders.LineStyle != -4142:
			if one_cell.Borders(7).LineStyle != -4142:
				# linestyle이 없으면 라인이 없는것으로 생각하고 나머지를 확인하지 않으면서 시간을 줄이는 것이다
				result["line_top_dic"]["style"] = one_cell.Borders(7).LineStyle
				result["line_top_dic"]["color"] = one_cell.Borders(7).Color
				result["line_top_dic"]["colorindex"] = one_cell.Borders(7).ColorIndex
				result["line_top_dic"]["thick"] = one_cell.Borders(7).Weight
				result["line_top_dic"]["tintandshade"] = one_cell.Borders(7).TintAndShade
			if one_cell.Borders(8).LineStyle != -4142:
				result["line_bottom_dic"]["style"] = one_cell.Borders(8).LineStyle
				result["line_bottom_dic"]["color"] = one_cell.Borders(8).Color
				result["line_bottom_dic"]["colorindex"] = one_cell.Borders(8).ColorIndex
				result["line_bottom_dic"]["thick"] = one_cell.Borders(8).Weight
				result["line_bottom_dic"]["tintandshade"] = one_cell.Borders(8).TintAndShade
			if one_cell.Borders(9).LineStyle != -4142:
				result["line_left_dic"]["style"] = one_cell.Borders(9).LineStyle
				result["line_left_dic"]["color"] = one_cell.Borders(9).Color
				result["line_left_dic"]["colorindex"] = one_cell.Borders(9).ColorIndex
				result["line_left_dic"]["thick"] = one_cell.Borders(9).Weight
				result["line_left_dic"]["tintandshade"] = one_cell.Borders(9).TintAndShade
			if one_cell.Borders(10).LineStyle != -4142:
				result["line_right_dic"]["style"] = one_cell.Borders(10).LineStyle
				result["line_right_dic"]["color"] = one_cell.Borders(10).Color
				result["line_right_dic"]["colorindex"] = one_cell.Borders(10).ColorIndex
				result["line_right_dic"]["thick"] = one_cell.Borders(10).Weight
				result["line_right_dic"]["tintandshade"] = one_cell.Borders(10).TintAndShade
			if one_cell.Borders(11).LineStyle != -4142:
				result["line_x1_dic"]["style"] = one_cell.Borders(11).LineStyle
				result["line_x1_dic"]["color"] = one_cell.Borders(11).Color
				result["line_x1_dic"]["colorindex"] = one_cell.Borders(11).ColorIndex
				result["line_x1_dic"]["thick"] = one_cell.Borders(11).Weight
				result["line_x1_dic"]["tintandshade"] = one_cell.Borders(11).TintAndShade
			if one_cell.Borders(12).LineStyle != -4142:
				result["line_x2_dic"]["style"] = one_cell.Borders(12).LineStyle
				result["line_x2_dic"]["color"] = one_cell.Borders(12).Color
				result["line_x2_dic"]["colorindex"] = one_cell.Borders(12).ColorIndex
				result["line_x2_dic"]["thick"] = one_cell.Borders(12).Weight
				result["line_x2_dic"]["tintandshade"] = one_cell.Borders(12).TintAndShade

		return result

	def read_including_date_type(self):

		result = self.sheet_obj.Range(self.sheet_obj.Cells(self.x1, self.y1),
									  self.sheet_obj.Cells(self.x2, self.y2)).Value
		return result

	def read_memo_for_cell(self, sheet_name, xyxy):
		"""
		입력영역의 처음 셀의 메모의 값을 읽어오는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_memo_for_cell(sheet_name="", xyxy="")
			<object_name>.read_memo_for_cell("sht1", [1,1,3,20])
			<object_name>.read_memo_for_cell("", "")
			<object_name>.셀의 메모를 돌려주는것
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		return range_obj.Comment.Text()

	def read_multi_cell(self, xyxy_l2d):
		if not isinstance(xyxy_l2d[0], list):
			xyxy_l2d = [xyxy_l2d]
		result = []
		for xyxy in xyxy_l2d:
			one_value = self.check_input_data(self.sheet_obj.Cells(self.x1, self.y1).Value)
			result.append(one_value)
		return result

	def read_multi_cell_for_sheet(self, sheet_name, xyxy_l2d):
		"""
		추가) 여러셀값을 한번에 갖고오는것도 넣음

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_multi_cell(sheet_name="", xyxy_l2d=[[1, 1], [2, 2]])
			<object_name>.read_multi_cell("", xyxy_l2d=[[1, 1], [2, 2]])
			<object_name>.read_multi_cell("sht1", xyxy_l2d=[[1, 1], [2, 2]])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		if not isinstance(xyxy_l2d[0], list):
			xyxy_l2d = [xyxy_l2d]
		result = []
		for xyxy in xyxy_l2d:
			x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
			one_value = self.check_input_data(sheet_obj.Cells(x1, y1).Value)
			result.append(one_value)
		return result

	def read_n_char_from_start(self, input_no):
		l2d = self.read()
		result = []
		for l1d in l2d:
			temp = []
			for one in l1d:
				if isinstance(one, str):
					temp.append(one[0:input_no])
				else:
					temp.append("")
			result.append(temp)

		return result

	def read_n_char_from_start_for_range(self, sheet_name, xyxy, input_no):
		"""
		자주 사용하는 자료의 변경 형태로, 셀값중 앞에서 n번째까지의 문자를 갖고와서 영역안의 자료를 리스트로 만드는 것입니다
		생각보다, 많이 사용하면서, 간단한것이라, 아마 불러서 사용하는것보다는 그냥 코드로 새롭게 작성하는경우가
		많겠지만, 그냥. . 그냥 만들어 보았다

		예를 들어 : 시군 구자료에서 앞의 2 글자만 분리해서 얻어오는 코드, 어떤자료중에 앞에서 몇번째것들만 갖고오고 싶을때

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_no:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_n_char_from_start_for_range(sheet_name="", xyxy="", input_no=7)
			<object_name>.read_n_char_from_start_for_range("", "", 7)
			<object_name>.read_n_char_from_start_for_range(sheet_name="sht1", xyxy="", input_no=7)
		"""
		l2d = self.read_value_for_range(sheet_name, xyxy)

		result = []
		for l1d in l2d:
			temp = []
			for one in l1d:
				if isinstance(one, str):
					temp.append(one[0:input_no])
				else:
					temp.append("")
			result.append(temp)

		return result

	def read_n_write_with_two_sheet(self, sheet_name, input_xno, input_l2d):
		"""
		현재 시트의 한줄을 읽어와서, 다른시트에 값을 넣는 경우
		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_xno: (int) 정수, x를 나타내는 가로줄의 번호, row의 숫자번호
		:param input_l2d:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_n_write_with_two_sheet(sheet_name="", input_xno=7, input_l2d=[[1,"sht1",3],[4,"sht3",6],[7,"sht10",9]])
			<object_name>.read_n_write_with_two_sheet("", 7, [[1,"sht1",3],[4,"sht3",6],[7,"sht10",9]])
			<object_name>.read_n_write_with_two_sheet(sheet_name="sht1", input_xno=7, input_l2d=[[1,"sht1",3],[4,"sht3",6],[7,"sht10",9]])
		"""
		sheet_obj = self.check_sheet_name("")
		one_list = self.read_xline(sheet_name, input_xno)[0]
		input_l2d = self.check_input_data(input_l2d)
		for l1d in input_l2d:
			read_no, write_sheet, write_xy = l1d
			sheet_obj.Cells(write_xy[0], write_xy[1]).Value =one_list[read_no - 1]

	def read_numberformat_for_range(self, sheet_name, xyxy):
		"""
		속성을 포함한 값을 읽어오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_numberformat(sheet_name="", xyxy="")
			<object_name>.read_numberformat("sht1", [1,1,3,20])
			<object_name>.read_numberformat("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		result = []
		for x in range(x1, x2 + 1):
			temp = []
			for y in range(y1, y2 + 1):
				one_dic = {}
				one_cell = sheet_obj.Cells(x, y)
				one_dic["y"] = x
				one_dic["x"] = y
				one_dic["value"] = one_cell.Value
				one_dic["value2"] = one_cell.Value2
				one_dic["text"] = one_cell.Text
				one_dic["formula"] = one_cell.Formula
				one_dic["formular1c1"] = one_cell.FormulaR1C1
				one_dic["numberformat"] = one_cell.NumberFormat
				temp.append(one_dic)
			result.append(temp)

		return result

	def read_opened_workbook_filenames(self):
		"""
		모든 열려있는 엑셀화일의 이름들을 갖고옵니다

		:return:
		"""
		return [one.Name for one in self.xlapp.Workbooks]

	def read_range_name(self, range_name):
		xyxy = self.get_address_for_range_name(range_name)
		result = self.read()
		return result

	def read_range_obj(self, input_range_obj):
		"""
		range_obj로 값을 읽어오는 것

		:param input_range_obj: (object) 객체, 영역을 객체로 나타내는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_range_obj(input_range_obj=obj1)
			<object_name>.read_range_obj(obj1)
			<object_name>.read_range_obj(input_range_obj=obj123)
		"""

		return input_range_obj.Value

	def read_same_value(self):
		temp_datas = self.read()
		result = []
		for xy_list_data in temp_datas:
			for one_data in xy_list_data:
				if one_data in result or one_data is None:
					pass
				else:
					result.append(one_data)
		self.delete_value()
		for num in range(len(result)):
			mox, namuji = divmod(num, self.x2 - self.x1 + 1)
			self.sheet_obj.Cells(self.x1 + namuji, self.y1 + mox).Value = result[num]
		return result

	def read_same_value_for_range(self, sheet_name, xyxy):
		"""
		선택한 자료중에서 고유한 자료만을 골라내는 것이다
		1. 관련 자료를 읽어온다
		2. 자료중에서 고유한것을 찾아낸다
		3. 선택영역에 다시 쓴다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_same_value(sheet_name="", xyxy="")
			<object_name>.read_same_value("sht1", [1,1,3,20])
			<object_name>.read_same_value("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		temp_datas = self.read_value_for_range("", xyxy)
		result = []
		for xy_list_data in temp_datas:
			for one_data in xy_list_data:
				if one_data in result or one_data is None:
					pass
				else:
					result.append(one_data)
		self.delete_value_for_range("", xyxy)
		for num in range(len(result)):
			mox, namuji = divmod(num, x2 - x1 + 1)
			sheet_obj.Cells(x1 + namuji, y1 + mox).Value = result[num]

		return result

	def read_selection(self):
		self.set_range("")
		return self.range_obj.Value

	def read_sheet_name_by_position_no(self, input_no):
		"""
		선택된 시트를 앞에서 몇번째로 이동시키는 것		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_index: (int) 정수 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_sheet_name_by_position_no(input_no=3)
			<object_name>.read_sheet_name_by_position_no(5)
			<object_name>.read_sheet_name_by_position_no(7)
		"""
		sheets_name = self.get_sheet_names()
		result = sheets_name[input_no - 1]
		return result

	def read_sheet_name_for_activesheet(self):
		"""
		read_name_for_activesheet()
		간략설명 : 현재의 활성화된 시트의 이름을 돌려준다
		출력형태 : 시트이름

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_sheet_name_for_activesheet()
		"""
		return self.xlApp.ActiveSheet.Name

	def read_textboxes_as_l1d(self):

		result = []
		for shape in self.sheet_obj.Shapes:
			if shape.Type == 17:  #
				text = shape.TextFrame.Characters().Text
				result.append(text)
		result = self.check_input_data(result)
		return result

	def read_unique_value(self):
		temp_datas = self.read()
		temp_result = []
		for one_list_data in temp_datas:
			for one_data in one_list_data:
				if one_data in temp_result or one_data is None:
					pass
				else:
					temp_result.append(one_data)
		self.delete_value()
		for num in range(len(temp_result)):
			mox, namuji = divmod(num, self.x2 - self.x1 + 1)
			self.sheet_obj.Cells(self.x1 + namuji, self.y1 + mox).Value = temp_result[num]

	def read_unique_value_for_range(self, sheet_name, xyxy):
		"""
		선택한 자료중에서 고유한 자료만을 골라내는 것이다
		1. 관련 자료를 읽어온다
		2. 자료중에서 고유한것을 찾아낸다
		3. 선택영역에 다시 쓴다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_unique_value(sheet_name="", xyxy="")
			<object_name>.read_unique_value("sht1", [1,1,3,20])
			<object_name>.read_unique_value("", "")
		"""
		temp_datas = self.read_value_for_range(sheet_name, xyxy)
		result = []
		for xy_list_data in temp_datas:
			for one_data in xy_list_data:
				if one_data in result or one_data is None:
					pass
				else:
					result.append(one_data)
		result = self.check_input_data(result)
		return result

	def read_usedrange(self):
		self.set_range_by_usedrange()
		result = self.range_obj.Value
		result = self.check_input_data(result)
		return result

	def read_usedrange_for_sheet(self, sheet_name):
		"""
		usedrange 안의 값을 갖고온다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_usedrange(sheet_name="")
			<object_name>.read_value_for_usedrange("sht1")
			<object_name>.read_value_for_usedrange("")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(sheet_obj.UsedRange.Address)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		result = range_obj.Value
		result = self.check_input_data(result)
		return result

	def read_value2(self):
		result = self.range_obj.Value2
		result = self.check_input_data(result)
		return result

	def read_value2_for_cell(self, sheet_name, xyxy):
		"""
		엑셀의 값중에서 화면에 보여지는 값을 읽어오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value2_for_cell(sheet_name="", xyxy="")
			<object_name>.read_value2_for_cell("sht1", [1,1,3,20])
			<object_name>.read_value2_for_cell("", "")
		"""
		return self.read_value2_for_cell(sheet_name, xyxy)

	def read_value2_for_range(self, sheet_name, xyxy):
		"""
		엑셀의 값중에서 화면에 보여지는 값을 읽어오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value2_for_range(sheet_name="", xyxy="")
			<object_name>.read_value2_for_range("sht1", [1,1,3,20])
			<object_name>.read_value2_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		result = range_obj.Value3
		result = self.check_input_data(result)
		return result

	def read_value3(self):
		result = self.range_obj.Value3
		result = self.check_input_data(result)
		return result

	def read_value3_for_cell(self, sheet_name, xyxy):
		"""
		읽어온값 자체를 변경하지 않고 그대로 읽어오는 것
		그자체로 text형태로 돌려주는것
		만약 스캔을 한 숫자가 ,를 잘못 .으로 읽었다면
		48,100 => 48.1로 엑셀이 바로 인식을 하는데
		이럴때 48.100으로 읽어와서 바꾸는 방법을 하기위해 사용하는 방법

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value3_for_cell(sheet_name="", xyxy="")
			<object_name>.read_value3_for_cell("sht1", [1,1,3,20])
			<object_name>.read_value3_for_cell("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		return sheet_obj.Cells(x1, y1).Text

	def read_value3_for_range(self, sheet_name, xyxy):
		"""
		엑셀의 값중에서 화면에 보여지는 값을 읽어오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value3_for_range(sheet_name="", xyxy="")
			<object_name>.read_value3_for_range("sht1", [1,1,3,20])
			<object_name>.read_value3_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		result = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2)).Value3
		result = self.check_input_data(result)
		return result

	def read_value_check_date_for_range(self, sheet_name, xyxy):
		"""
		영역의 자료를 읽어와서
		- 모든 자료를 리스트로 바꿔준다
		- 날짜와 시간의 자료가 있으면, 의미가있는 영역까지만 나타냄

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			   <object_name>.read_value_check_date(sheet_name="", xyxy="")
			   <object_name>.read_value_check_date("sht1", [1,1,3,20])
			   <object_name>.read_value_check_date("", "")
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		result =self.check_input_data(range_obj.Value)
		return result

	def read_value_for_activecell(self):
		"""
		현재셀의 값을 돌려주는것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_activecell()
		"""
		result = self.xlapp.ActiveCell.Value2
		result = self.check_input_data(result)
		return result

	def read_value_for_activecell_n_yno(self, input_yno):
		"""
		현재 선택된 셀의 x번호와 입력받은 y줄의 번호를 조합한 셀의 값을 읽어오는것

		:param input_yno: (int) 정수, 엑셀의 세로열(column) 번호를 나타내는것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_activecell_n_yno(3)
		"""
		xyxy = self.get_address_for_activecell()
		value = self.read_value_for_cell("", [xyxy[0], input_yno])
		value = self.check_input_data(value)
		return value

	def read_value_for_cell(self, sheet_name, xyxy):
		"""
		주) value -> value2
		값을 일정한 영역에서 갖고온다
		만약 영역을 두개만 주면 처음과 끝의 영역을 받은것으로 간주해서 알아서 처리하도록 변경하였다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_cell(sheet_name="", xyxy="")
			<object_name>.read_value_for_cell("sht1", [1,1,3,20])
			<object_name>.read_value_for_cell("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		one_value = sheet_obj.Cells(x1, y1).Value
		one_value = self.check_input_data(one_value)
		return one_value

	def read_value_for_cell_as_text(self, sheet_name, xyxy):
		"""
		읽어온값 자체를 변경하지 않고 그대로 읽어오는 것
		그자체로 text형태로 돌려주는것
		만약 스캔을 한 숫자가 ,를 잘못 .으로 읽었다면
		48,100 => 48.1로 엑셀이 바로 인식을 하는데
		이럴때 48.100으로 읽어와서 바꾸는 방법을 하기위해 사용하는 방법

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_cell_as_text(sheet_name="", xyxy="")
			<object_name>.read_value_for_cell_as_text("sht1", [1,1,3,20])
			<object_name>.read_value_for_cell_as_text("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		return sheet_obj.Cells(x1, y1).Text

	def read_value_for_continuous_range(self, sheet_name, xyxy):
		"""
		read_continuousrange_value(sheet_name="", xyxy="")
		현재선택된 셀을 기준으로 연속된 영역을 가지고 오는 것입니다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_continuous_range(sheet_name="", xyxy="")
			<object_name>.read_value_for_continuous_range("sht1", [1,1,3,20])
			<object_name>.read_value_for_continuous_range("", "")
		"""
		row = xyxy
		col = xyxy
		sheet_obj = self.xlBook.Worksheets(sheet_name)
		bottom = row  # 아래의 행을 찾는다
		while sheet_obj.Cells(bottom + 1, col).Value not in [None, '']:
			bottom = bottom + 1
		right = col  # 오른쪽 열
		while sheet_obj.Cells(row, right + 1).Value not in [None, '']:
			right = right + 1
		result =  sheet_obj.Range(sheet_obj.Cells(row, col), sheet_obj.Cells(bottom, right)).Value
		result = self.check_input_data(result)
		return result

	def read_value_for_multi_cell(self, sheet_name, xyxy_l2d):
		"""
		추가) 여러셀값을 한번에 갖고오는것도 넣음

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_in_multi_cell(sheet_name="", xyxy_l2d=[[1, 1], [2, 2]])
			<object_name>.read_value_in_multi_cell("", xyxy_l2d=[[1, 1], [2, 2]])
			<object_name>.read_value_in_multi_cell("sht1", xyxy_l2d=[[1, 1], [2, 2]])
		"""
		if not isinstance(xyxy_l2d[0], list):
			xyxy_l2d = [xyxy_l2d]
		result = []
		for xyxy in xyxy_l2d:
			sheet_obj = self.check_sheet_name(sheet_name)
			x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
			one_value = sheet_obj.Cells(x1, y1).Value
			if isinstance(one_value, int):
				one_value = int(one_value)
			elif one_value == None:
				one_value = ""
			result.append(one_value)
		result = self.check_input_data(result)
		return result

	def read_value_for_range(self, sheet_name, xyxy):
		"""
		영역의 값을 갖고온다
		주) 원래는 value였으나 pyside6에서 코딩중에 날짜부분이 문제가 일으키는데 value2로 변경하니 문제가 없어서 변경함

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_range(sheet_name="", xyxy="")
			<object_name>.read_value_for_range("sht1", [1,1,3,20])
			<object_name>.read_value_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		result = self.util.change_any_type_to_l2d(range_obj.Value)
		result = self.check_input_data(result)
		return result

	def read_value_for_range_as_dic_with_xy_position(self, sheet_name, xyxy):
		"""
		선택된 영역안의 2차원자료를 사전형식으로 돌려 주는 것
		같은값을 발견하면, 주소를 추가하는 형태
		예: [["가나","다라"],["ab", "다라"]] => {"가나":[[1,1]], "다라":[[1,2], [2,2]],"ab":[[2,1]]}

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_range_as_dic_with_xy_position(sheet_name="", xyxy="")
			<object_name>.read_value_for_range_as_dic_with_xy_position("sht1", [1,1,3,20])
			<object_name>.read_value_for_range_as_dic_with_xy_position("", "")
		"""
		result = {}
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		l2d = range_obj.Value

		for ix, l1d in enumerate(l2d):
			for iy, one_value in enumerate(l1d):
				if one_value in result.keys():
					result[ix + 1, iy + 1].append([one_value])
				else:
					result[one_value] = [[ix + 1, iy + 1]]
		result = self.check_input_data(result)
		return result

	def read_value_for_range_as_l1d_for_xline_base(self, sheet_name, xyxy):
		"""
		2 차원의 자료를 1차원으로 만드는 것이며, 가로로 이동하면서 읽는 형식

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_xyxy_as_l1d_for_xline_base(sheet_name="", xyxy="")
			<object_name>.read_xyxy_as_l1d_for_xline_base("sht1", [1,1,3,20])
			<object_name>.read_xyxy_as_l1d_for_xline_base("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		result = []
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Value
				result.append(one_value)
		result = self.check_input_data(result)
		return result

	def read_value_for_range_as_l1d_for_yline_base(self, sheet_name, xyxy):
		"""
		2차원의 자료를 1차원으로 만드는 것이며, 세로로 내려가면서 읽는 형식

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_xyxy_as_l1d_for_yline_base(sheet_name="", xyxy="")
			<object_name>.read_xyxy_as_l1d_for_yline_base("sht1", [1,1,3,20])
			<object_name>.read_xyxy_as_l1d_for_yline_base("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		result = [sheet_obj.Cells(x, y).Value for y in range(y1, y2 + 1) for x in range(x1, x2 + 1)]

		return result

	def read_value_for_range_as_list(self, sheet_name, xyxy):
		"""
		2차원의 듀플을 2차원 리스트로 만드는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_range_as_list(sheet_name="", xyxy="")
			<object_name>.read_value_for_range_as_list("sht1", [1,1,3,20])
			<object_name>.read_value_for_range_as_list("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		l2d = range_obj.Value

		result = []
		for x in range(len(l2d)):
			temp = []
			for y in range(len(l2d[0])):
				value = l2d[x][y]
				if value:
					pass
				else:
					value = ""
				temp.append(value)
			result.append(temp)
		result = self.check_input_data(result)
		return result

	def read_value_for_range_as_text(self, sheet_name, xyxy):
		"""
		읽어온값 자체를 변경하지 않고 그대로 읽어오는 것 그자체로 text 형태로 돌려주는것 만약 스캔을 한 숫자가 .를 잘못 .으로 읽었다면
		48,100 => 48.1로 엑셀이 바로 인식을 하는데 이럴때 48.100 으로 읽어와서 바꾸는 방법을 하기위해 사용하는 방법

		:param sheet_ name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_range_as_text(sheet_name="", xyxy="")
			<object_name>.read_value_for_range_as_text("sht1", [1,1,3,20])
			<object_name>.read_value_for_range_as_text("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		result = []
		for x in range(x1, x2 + 1):
			temp = []
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Text
				temp.append(one_value)
			result.append(temp)
		return result

	def read_value_for_range_for_continuous_same_value(self, sheet_name, xyxy):
		"""
		현재선택된 셀을 기준으로 연속된 영역을 가지고 오는 것입니다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_range_for_continuous_same_value(sheet_name="", xyxy="")
			<object_name>.read_value_for_range_for_continuous_same_value("sht1", [1,1,3,20])
			<object_name>.read_value_for_range_for_continuous_same_value("", "")
		"""
		row = xyxy
		col = xyxy
		sheet_obj = self.check_sheet_name(sheet_name)
		bottom = row  # 아래의 행을 찾는다
		while sheet_obj.Cells(bottom + 1, col).Value not in [None, '']:
			bottom = bottom + 1
		right = col  # 오른쪽 열
		while sheet_obj.Cells(row, right + 1).Value not in [None, '']:
			right = right + 1
		result =  sheet_obj.Range(sheet_obj.Cells(row, col), sheet_obj.Cells(bottom, right)).Value
		result = self.check_input_data(result)
		return result

	def read_value_for_range_for_unique_value(self, sheet_name, xyxy):
		"""
		선택한 자료중에서 고유한 자료만을 골라내는 것이다
		1. 관련 자료를 읽어온다
		2. 자료중에서 고유한것을 찾아낸다
		3. 선택영역에 다시 쓴다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_range_for_unique_value(sheet_name="", xyxy="")
			<object_name>.read_value_for_range_for_unique_value("sht1", [1,1,3,20])
			<object_name>.read_value_for_range_for_unique_value("", "")
		"""
		l2d = self.read_value_for_range(sheet_name, xyxy)
		result = set()
		for l1d in l2d:
			for one_value in l1d:
				if one_value:
					result.add(one_value)
		result = self.check_input_data(list(result))
		return result

	def read_value_for_range_name(self, sheet_name, range_name):
		"""
		이름영역으로 값을 읽어오는 것
		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param range_name: (str) 입력으로 들어오는 텍스트, 영역이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_range_name(sheet_name="", range_name="name1")
			<object_name>.read_value_for_range_name("", range_name="name1")
			<object_name>.read_value_for_range_name("sht1", range_name="name1")
		"""
		xyxy = self.read_address_for_range_name(sheet_name, range_name)
		result = self.read_value_for_range(sheet_name, xyxy)
		return result

	def read_value_for_range_with_numberformat(self, sheet_name, xyxy):
		"""
		속성을 포함한 값을 읽어오는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_range_with_numberformat(sheet_name="", xyxy="")
			<object_name>.read_value_for_range_with_numberformat("sht1", [1,1,3,20])
			<object_name>.read_value_for_range_with_numberformat("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		result = []
		for x in range(x1, x2 + 1):
			temp = []
			for y in range(y1, y2 + 1):
				one_dic = {}
				one_cell = sheet_obj.Cells(x, y)
				one_dic["y"] = x
				one_dic["x"] = y
				one_dic["value"] = one_cell.Value
				one_dic["value2"] = one_cell.Value2
				one_dic["text"] = one_cell.Text
				one_dic["formula"] = one_cell.Formula
				one_dic["formular1c1"] = one_cell.FormulaR1C1
				one_dic["numberformat"] = one_cell.NumberFormat
				temp.append(one_dic)
			result.append(temp)
		result = self.check_input_data(result)
		return result

	def read_value_for_range_with_xy_headers(self, sheet_name, xyxy):
		"""
		영역의 값을 갖고온다. 맨앞과 위에 번호로 행과열을 추가한다
		가끔은 자료중에서 필요없는것을 삭제했더니, 원래 있었던 자료의 위치를 알수가 없어서, 만들어 본것임

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_range_with_xy_headers(sheet_name="", xyxy="")
			<object_name>.read_value_for_range_with_xy_headers("sht1", [1,1,3,20])
			<object_name>.read_value_for_range_with_xy_headers("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		top_line = list(range(y1 - 1, y2 + 1))

		all_data = list(range_obj.Value2)
		result = []
		for x in range(0, x2 - x1 + 1):
			temp = [x + 1]
			temp.extend(list(all_data[x]))
			result.append(temp)
		result.insert(0, top_line)
		result = self.check_input_data(result)
		return result

	def read_value_for_selection(self, sheet_name):
		"""
		값을 일정한 영역에서 갖고온다
		만약 영역을 두개만 주면 처음과 끝의 영역을 받은것으로 간주해서 알아서 처리하도록 변경하였다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_in_selection(sheet_name="")
			<object_name>.read_value_in_selection("sht1")
			<object_name>.read_value_in_selection("")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy("")
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		result = range_obj.Value
		result = self.check_input_data(result)
		return result

	def read_value_for_textboxes_as_l1d(self, sheet_name):
		"""
		모든 텍스트 박스의 값을 읽어보는 것
		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_textboxes_as_l1d(sheet_name="")
			<object_name>.read_value_for_textboxes_as_l1d("sht1")
			<object_name>.read_value_for_textboxes_as_l1d("")
		"""
		result = []
		sheet_obj = self.check_sheet_name(sheet_name)
		for shape in sheet_obj.Shapes:
			if shape.Type == 17:  #
				text = shape.TextFrame.Characters().Text
				result.append(text)
		result = self.check_input_data(result)
		return result

	def read_value_for_usedrange(self, sheet_name):
		"""
		usedrange 안의 값을 갖고온다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_usedrange(sheet_name="")
			<object_name>.read_value_for_usedrange("sht1")
			<object_name>.read_value_for_usedrange("")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		xyxy = self.change_any_address_to_xyxy(sheet_obj.UsedRange.Address)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		result = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2)).Value
		result = self.check_input_data(result)
		return result

	def read_value_for_xline(self, sheet_name, xx_list):
		"""
		한줄인 x라인 의 모든값을 읽어온다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xx_list: (list) 가로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_in_xline(sheet_name="", xx_list=[3,5])
			<object_name>.read_value_in_xline("", [1,7])
			<object_name>.read_value_in_xline(sheet_name="sht1", xx_list=[3,5])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, x2 = self.check_xx_address(xx_list)
		result = sheet_obj.Range(sheet_obj.Cells(x1, 1), sheet_obj.Cells(x1, 1)).EntireRow.Value2
		result = self.check_input_data(result)
		return result

	def read_value_for_xline_at_activecell(self):
		"""
		현재 활성화된 셀이 있는 한줄을 읽어옵니다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_in_xline_at_activecell()
		"""
		sheet_obj = self.check_sheet_name("")
		xyxy = self.change_any_address_to_xyxy(self.xlapp.ActiveCell.Address)
		result = sheet_obj.Cells(xyxy[0], 1).EntireRow.Value2[0]
		result = self.check_input_data(result)
		return result

	def read_value_for_xxline(self, sheet_name, xx_list):
		"""
		xx_list라인의 모든값을 읽어온다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xx_list: (list) 가로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_in_xxline(sheet_name="", xx_list=[3,5])
			<object_name>.read_value_in_xxline("", [1,7])
			<object_name>.read_value_in_xxline(sheet_name="sht1", xx_list=[3,5])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		result = sheet_obj.Range(sheet_obj.Cells(xx_list[0], 1),
								 sheet_obj.Cells(xx_list[1], 1)).EntireRow.Value2
		result = self.check_input_data(result)
		return result

	def read_value_for_xywh(self, sheet_name, input_xywh):
		"""
		시작점을 기준으로 가로세로의 갯수만큼의 값을 읽어오는 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_xywh:  (list or str) 입력으로 들어오는 주소값으로 형태이며, 문자열의 형태나 리스트형태가 가능하다. 보통 [1,1,2,2]의형태이며, ""을 입력한 경우는 주소를 계산하는 부분에서 현재 선택영역을 기준으로 리스트형태로 만든다
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_for_xywh(sheet_name="sht1", input_xywh=[3,4,20,35]e)
			<object_name>.read_value_for_xywh("sht2", [1,1,30,20])
			<object_name>.read_value_for_xywh("sht1", [1,1,10,20])
		"""
		xyxy = [input_xywh[0], input_xywh[1], input_xywh[0] + input_xywh[2] - 1, input_xywh[1] + input_xywh[3] - 1]
		result = self.read_value_for_range(sheet_name, xyxy)
		result = self.check_input_data(result)
		return result

	def read_value_for_yline(self, sheet_name, yy_list):
		"""
		한줄인 y라인의 모든값을 읽어온다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param yy_list: (list) 세로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_in_yline(sheet_name="", yy_list=[2, 4])
			<object_name>.read_value_in_yline("", [2, 4])
			<object_name>.read_value_in_yline("sht1", [3,7])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		y1, y2 = self.check_yy_address(yy_list)
		result = sheet_obj.Range(sheet_obj.Cells(1, y1),
								 sheet_obj.Cells(1, y1)).EntireColumn.Value2

		result = self.check_input_data(result)
		return result

	def read_value_for_yline_at_activecell(self, sheet_name):
		"""
		사용된 범위안에서 현재셀이 선택된 y 라인 한줄을 갖고오는 것 영역을 가르킬때는 가장 왼쪽위의 셀을 기준으로 한다
		"""
		xyxy = self.read_address_for_activecell()
		xyxy2 = self.read_address_for_usedrange(sheet_name)
		result = self.read_value_for_range(sheet_name, [1, xyxy[1], 1, xyxy2[2]])[0]
		result = self.check_input_data(result)
		return result

	def read_value_for_yyline(self, sheet_name, yy_list):
		"""
		read_yyline_value(sheet_name="", xx_list)
		가로줄들의 전체의 값을 읽어온다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param yy_list: (list) 세로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_in_yyline(sheet_name="", yy_list=[2, 4])
			<object_name>.read_value_in_yyline("", [2, 4])
			<object_name>.read_value_in_yyline("sht1", [3,7])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		result = sheet_obj.Range(sheet_obj.Cells(yy_list[0], 1), sheet_obj.Cells(yy_list[1], 1)).EntireRow.Value
		result = self.check_input_data(result)
		return result

	def read_value_including_date_type(self, sheet_name, xyxy):
		"""
		영역의 값을 갖고온다
		단, 날짜 type의 그 자체로 읽어오는 것이다
		주) 원래는 value였으나 pyside6에서 코딩중에 날짜부분이 문제가 일으키는데 value2로 변경하니 문제가 없어서 변경함

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_value_including_date_type(sheet_name="", xyxy="")
			<object_name>.read_value_including_date_type("sht1", [1,1,3,20])
			<object_name>.read_value_including_date_type("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		result = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2)).Value
		return result

	def read_with_numberformat(self):
		result = []
		for x in range(self.x1, self.x2 + 1):
			temp = []
			for y in range(self.y1, self.y2 + 1):
				one_dic = {}
				one_cell = self.sheet_obj.Cells(x, y)
				one_dic["y"] = x
				one_dic["x"] = y
				one_dic["value"] = one_cell.Value
				one_dic["value2"] = one_cell.Value2
				one_dic["text"] = one_cell.Text
				one_dic["formula"] = one_cell.Formula
				one_dic["formular1c1"] = one_cell.FormulaR1C1
				one_dic["numberformat"] = one_cell.NumberFormat
				temp.append(one_dic)
			result.append(temp)
		result = self.check_input_data(result)
		return result

	def read_with_xy_headers(self):
		top_line = list(range(self.y1 - 1, self.y2 + 1))

		all_data = list(self.range_obj.Value2)
		result = []
		for x in range(0, self.x2 - self.x1 + 1):
			temp = [x + 1]
			temp.extend(list(all_data[x]))
			result.append(temp)
		result.insert(0, top_line)
		result = self.check_input_data(result)
		return result

	def read_xxline(self, xx_list):
		if xx_list:
			temp = self.check_input_area(xx_list)
			if len(temp) == 1:
				x1 = temp[0]
				x2 = temp[0]
			elif len(temp) == 2:
				x1 = temp[0]
				x2 = temp[1]
			elif len(temp) == 4:
				x1 = temp[0]
				x2 = temp[2]
		else:
			x1 = self.x1
			x2 = self.x2

		xyxy = self.get_address_for_intersect_with_usedrange([x1, 0, x2, 0])
		self.set_range(xyxy)
		l2d = self.read()
		return l2d

	def read_yline(self, sheet_name, yy_list):
		"""
		한줄인 y라인의 모든값을 읽어온다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param yy_list: (list) 세로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.read_yline(sheet_name="", yy_list=[2, 4])
			<object_name>.read_yline("", [2, 4])
			<object_name>.read_yline("sht1", [3,7])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		y1, y2 = self.check_yy_address(yy_list)
		result = sheet_obj.Range(sheet_obj.Cells(1, y1), sheet_obj.Cells(1, y1)).EntireColumn.Value2

		result = self.check_input_data(result)
		return result

	def read_yline_at_activecell(self, sheet_name):
		"""
		사용된 범위안에서 현재셀이 선택된 y 라인 한줄을 갖고오는 것 영역을 가르킬때는 가장 왼쪽위의 셀을 기준으로 한다
		"""
		xyxy = self.get_address_for_activecell()
		xyxy2 = self.get_address_for_usedrange(sheet_name)
		result = self.read_value_for_range(sheet_name, [1, xyxy[1], 1, xyxy2[2]])[0]
		result = self.check_input_data(result)
		return result

	def read_yyline(self, yy_list):
		if yy_list:
			temp = self.check_input_area(yy_list)
			if len(temp) == 1:
				y1 = temp[0]
				y2 = temp[0]
			elif len(temp) == 2:
				y1 = temp[0]
				y2 = temp[1]
			elif len(temp) == 4:
				y1 = temp[0]
				y2 = temp[2]
		else:
			y1 = self.y1
			y2 = self.y2

		xyxy = self.get_address_for_intersect_with_usedrange([0, y1, 0, y2])
		self.set_range(xyxy)
		l2d = self.read()
		return l2d

	def regroup_l2d_by_each_nea(self, input_l2d, input_index):
		"""
		2차원의 자료를 번호를 기준으로 그룹화하는것

		:param input_l2d: (list) 2차원의 list형 자료
		:param input_index: (int) 0부터 시작하는 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.regroup_l2d_by_each_nea(input_l2d=[[1, 2], [4, 5]], input_index=4)
			<object_name>.regroup_l2d_by_each_nea([[1, 2], [4, 5]], 4)
			<object_name>.regroup_l2d_by_each_nea(input_l2d=[[1, 2], [4, 5]], input_index=3)
		"""
		result = []
		# 2차원자료를 원하는 열을 기준으로 정렬
		input_l2d = self.check_input_data(input_l2d)
		sorted_input_l2d = self.sort_l2d_by_index(input_l2d, input_index)

		check_value = sorted_input_l2d[0][input_index]
		temp = []
		for one_list in sorted_input_l2d:
			if one_list[input_index] == check_value:
				temp.append(one_list)
			else:
				result.append(temp)
				temp = [one_list]
				check_value = one_list[input_index]
		if temp:
			result.append(temp)
		return result

	def remain_unique_value(self):
		temp_datas = self.read()
		temp_result = []
		for one_list_data in temp_datas:
			for one_data in one_list_data:
				if one_data in temp_result or one_data is None:
					pass
				else:
					temp_result.append(one_data)

		self.delete_value()
		for num in range(len(temp_result)):
			mok, namuji = divmod(num, self.y2 - self.y1 + 1)
			self.sheet_obj.Cells(self.x1 + mok, self.y1 + namuji).Value = temp_result[num]

	def remain_unique_value_for_range(self, sheet_name, xyxy):
		"""
		선택한 영역의 자료를 읽어와서, 자료중에서 고유한 자료만을 골라내낸후
		다시 그영역에 쓰는것

		1. 관련 자료를 읽어온다-------
		2. 자료중에서 고유한것을 찾아낸다
		3. 선택영역에 다시 쓴다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.remain_unique_value_for_range(sheet_name="", xyxy="")
			<object_name>.remain_unique_value_for_range("sht1", [1,1,3,20])
			<object_name>.remain_unique_value_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		temp_datas = self.read_value_for_range(sheet_name, xyxy)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		temp_result = []
		for one_list_data in temp_datas:
			for one_data in one_list_data:
				if one_data in temp_result or one_data is None:
					pass
				else:
					temp_result.append(one_data)

		self.delete_value_for_range(sheet_name, xyxy)
		for num in range(len(temp_result)):
			mok, namuji = divmod(num, y2 - y1 + 1)
			sheet_obj.Cells(x1 + mok, y1 + namuji).Value = temp_result[num]

	def remove_paint_for_range(self, sheet_name, xyxy):
		"""
		셀의 배경색을 color_name형식으로 칠하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.remove_paint_for_range(sheet_name="", xyxy="")
			<object_name>.remove_paint_for_range("", "")
			<object_name>.remove_paint_for_range(sheet_name="sht1", xyxy="")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Interior.ColorIndex = 0

	def replace_first_char(self, input_l2d, one_char):

		input_l2d = self.check_input_data(input_l2d)
		to_be_changed = [one[0] for one in input_l2d]

		for x in range(self.x1, self.x2 + 1):
			for y in range(self.y1, self.y2 + 1):
				try:
					one_value = self.sheet_obj.Cells(x, y).Value
					one_char = str(one_value[0])
					if one_value[0] in to_be_changed:
						for l1d in input_l2d:
							one_char = one_char.replace(l1d[0], l1d[1])
					self.sheet_obj.Cells(x, y).Value = one_char + one_value[1:]
				except:
					pass

	def replace_first_char_for_range(self, sheet_name, xyxy, input_l2d):
		"""
		가끔 맨 앞글자만 바꾸고 싶을때가 있다
		그럴때 사용하는 것으로, 한번에 여러개도 가능하도록 만들었다

		사용법 : change_first_char("", [1,1,100,1], [["'", ""], ["*", ""], [" ", ""],])

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_l2d: (list) 2차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.replace_first_char_for_range(sheet_name, xyxy, input_l2d)
			<object_name>.replace_first_char_for_range("", "", [[1, 2], [4, 5]])
			<object_name>.replace_first_char_for_range(sheet_name="sht1", xyxy="", input_l2d=[[1, 2], [4, 5]])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		input_l2d = self.check_input_data(input_l2d)
		to_be_changed = [one[0] for one in input_l2d]

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				try:
					one_value = sheet_obj.Cells(x, y).Value
					one_char = str(one_value[0])
					if one_value[0] in to_be_changed:
						for l1d in input_l2d:
							one_char = one_char.replace(l1d[0], l1d[1])
					sheet_obj.Cells(x, y).Value = one_char + one_value[1:]
				except:
					pass

	def replace_last_char(self, input_l2d, one_char):
		input_l2d = self.check_input_data(input_l2d)

		to_be_changed = []
		for one in input_l2d:
			to_be_changed.append(one[0])

		for x in range(self.x1, self.x2 + 1):
			for y in range(self.y1, self.y2 + 1):
				one_value = self.sheet_obj.Cells(x, y).Value2
				one_char = str(one_value[-1])
				if one_value[-1] in to_be_changed:
					for l1d in input_l2d:
						one_char = one_char.replace(l1d[0], l1d[1])
				self.sheet_obj.Cells(x, y).Value = one_value[:-1] + one_char

	def replace_last_char_for_range(self, sheet_name, xyxy, input_l2d):
		"""
		가끔 맨 뒷글자만 바꾸고 싶을때가 있다
		그럴때 사용하는 것으로, 한번에 여러개도 가능하도록 만들었다
		사용법 : ("", [1,1,100,1], [["'", ""], ["*", ""], [" ", ""],])

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_l2d: (list) 2차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.replace_last_char_for_range(sheet_name, xyxy, input_l2d)
			<object_name>.replace_last_char_for_range("", "", [[1, 2], [4, 5]])
			<object_name>.replace_last_char_for_range(sheet_name="sht1", xyxy="", input_l2d=[[1, 2], [4, 5]])
		"""
		input_l2d = self.check_input_data(input_l2d)
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		to_be_changed = []
		for one in input_l2d:
			to_be_changed.append(one[0])

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Value2
				one_char = str(one_value[-1])
				if one_value[-1] in to_be_changed:
					for l1d in input_l2d:
						one_char = one_char.replace(l1d[0], l1d[1])
				sheet_obj.Cells(x, y).Value = one_value[:-1] + one_char

	def replace_many_word(self, input_list):
		self.replace_many_word(input_list)

	def replace_many_word_for_range(self, sheet_name, xyxy, input_list):
		"""
		한번에 여러 갯수를 바꾸는 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.replace_many_word_for_range(sheet_name="", xyxy="", input_list=[1, "abc", "가나다"])
			<object_name>.replace_many_word_for_range("", "", [1, "abc", "가나다"])
			<object_name>.replace_many_word_for_range("sht1", "", [1, "abc", "가나다"])
		"""
		input_list = self.check_input_data(input_list)
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				one_value = str(self.read_value_for_cell(sheet_name, [x, y]))
				if one_value:
					for one_xylist in input_list:
						one_value = one_value.replace(one_xylist[0], one_xylist[1])
					sheet_obj.Cells(x, y).Value = one_value

	def replace_with_xre_as_selection_directly(self, input_xre, replace_text):
		"""
		엑셀의 선택한 부분을 그대로 변경하는 것

		:param input_xre: (str) xre형식의 문자열
		:param replace_text: (str) 입력으로 들어오는 텍스트, 바꿀 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.replace_with_xre_as_selection_directly(input_xre="[시작:처음][영어:1~4][한글:3~10]", replace_text="입력값")
			<object_name>.replace_with_xre_as_selection_directly("[시작:처음][영어:1~4][한글:3~10]", "입력값2")
			<object_name>.replace_with_xre_as_selection_directly(input_xre="[시작:처음][영어:1~4][한글:3~10]", replace_text="입력값3")
		"""
		sheet_obj = self.check_sheet_name("")
		xyxy = self.get_address_for_selection()

		for x in range(xyxy[0], xyxy[2] + 1):
			for y in range(xyxy[1], xyxy[3] + 1):
				value = sheet_obj.Cells(x, y).Value
				sheet_obj.Cells(x, y).Value = self.rex.replace_with_xsql(input_xre, replace_text, value)

	def reset_data(self):
		self.value = None
		self.sheet_obj = None
		self.sheet_obj2 = None

		self.range_obj = None
		self.range_obj2 = None

		self.x = None
		self.y = None
		self.x0 = None
		self.y0 = None

		self.x1 = None
		self.y1 = None
		self.x2 = None
		self.y2 = None

		self.x3 = None
		self.y3 = None
		self.x4 = None
		self.y4 = None

	def resize_data_for_range(self, input_l2d, xyxy):
		"""
		xyxy영역안에만 자료를 만들려고 할때, 이영역안의 맞도록 자료를 변경하는 것

		:param l2d: (list) 2차원의 list형 자료
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.resize_data_for_range(input_l2d=[[1, 2], [4, 5]], xyxy=[1, 3, 3, 12])
			<object_name>.resize_data_for_range([[1, 2], [4, 5]], [1, 3, 3, 12])
			<object_name>.resize_data_for_range(input_l2d=[[1, 2], [4, 5]], xyxy=[1, 1, 3, 12])
		"""
		result = []
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		input_l2d = self.check_input_data(input_l2d)

		if len(input_l2d) > x2 - x1 + 1:
			input_l2d = input_l2d[:x2 - x1 + 1]

		for l1d in input_l2d:
			if len(l1d) > y2 - y1 + 1:
				l1d = l1d[:y2 - y1 + 1]
			result.append(l1d)
		return result

	def resize_image_to_fit_xyxy(self, image_no, image_ratio_lock_tf):
		aaa = self.get_pxywh()
		bbb = self.count_shape_for_sheet(image_no, aaa[2], aaa[3], image_ratio_lock_tf)
		self.move_shape_position(image_no, aaa[1], aaa[0])

	def resize_image_to_fit_xyxy_for_sheet(self, sheet_name, xyxy, image_no=5, image_ratio_lock_tf=True):
		"""
		엑셀의 사진을 입력영역에 맞게 이동시키고 크기를 맞추는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param image_no: (int) 이미지를 나타내는 1부터 시작하는 숫자 번호
		:param image_ratio_lock_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.resize_image_to_fit_xyxy(sheet_name="", xyxy="", image_no=5, image_ratio_lock_tf=True)
			<object_name>.resize_image_to_fit_xyxy("", "", 5, True)
			<object_name>.resize_image_to_fit_xyxy(sheet_name="sht1", xyxy=[1,1,5,7], image_no=5, image_ratio_lock_tf=True)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		aaa = self.get_pxywh_for_range(sheet_name, xyxy)
		bbb = self.count_shape_for_sheet(sheet_name, image_no, aaa[2], aaa[3], image_ratio_lock_tf)
		self.move_shape_position(sheet_name, image_no, aaa[1], aaa[0])

	def resize_l2d_for_range(self, input_l2d, xyxy):
		"""
		영역에 맞도록 입력 자룔를 이영역안의 맞도록 자료를 변경하는 것
		만약 xyxy가 더 크면, None을 집어 넣는다

		:param input_l2d: (list) 2차원의 list형 자료
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.resize_l2d_for_range(input_l2d=[[1, 2], [4, 5]], xyxy=[1, 3, 3, 12])
			<object_name>.resize_l2d_for_range([[1, 2], [4, 5]], [1, 3, 3, 12])
			<object_name>.resize_l2d_for_range(input_l2d=[[1, 2], [4, 5]], xyxy=[1, 1, 3, 12])
		"""
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		input_l2d = self.check_input_data(input_l2d)

		result = self.util.resize_l2d(input_l2d, 0, 0, (x2 - x1), (y2 - y1))
		return result

	def reverse_l2d_top_n_bottom(self):
		t2d = self.read()
		result = self.util.change_xylist_to_yxlist(t2d)
		return result

	def reverse_l2d_top_n_bottom_for_range(self, sheet_name, xyxy):
		"""
		2차원자료를 뒤집는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.reverse_l2d_top_n_bottom(sheet_name="", xyxy="")
			<object_name>.reverse_l2d_top_n_bottom("sht1", [1,1,3,20])
			<object_name>.reverse_l2d_top_n_bottom("", "")
		"""
		t2d = self.read_value_for_range(sheet_name, xyxy)
		result = self.change_xylist_to_list(t2d)
		return result

	def rotate_shape_by_name(self, input_shape_obj, rotation_degree=90):
		"""
		도형을 회전시키는 것
		도형은 중간을 기준으로 회전을 합니다

		:param input_shape_obj: (object) 객체,
		:param rotation_degree: (int) 360도를 기준으로 회전할 숫자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.rotate_shape_by_name(input_shape_obj="object1", rotation_degree=90)
			<object_name>.rotate_shape_by_name("object1", 90)
			<object_name>.rotate_shape_by_name(input_shape_obj="object1", rotation_degree=40)
		"""
		input_shape_obj.Rotation = rotation_degree

	def round_float_from_nth_position(self, input_no):
		# 파이썬의 round(number, n) 함수는 number를 소수점 n자리까지 반올림합니다.

		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = self.sheet_obj.Cells(x, y).Value
			if isinstance(one_value, float):
				rounded_value = round(one_value, input_no)
				self.sheet_obj.Cells(x, y).Value = rounded_value

	def round_float_from_nth_position_for_range(self, sheet_name, xyxy, input_no):
		"""
		입력된 숫자를 소수점 아래 n번째 자리까지 남기고 반올림합니다.
		(n+1)번째 자리에서 반올림이 수행됩니다.

		:param number: 반올림할 실수 값입니다.
		:param n: 남길 소수 자릿수입니다 (소수점 아래 n번째까지 남김).
		:return: 반올림된 실수 값입니다.
		"""
		# 파이썬의 round(number, n) 함수는 number를 소수점 n자리까지 반올림합니다.
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
				for y in range(y1, y2 + 1):
					one_value = sheet_obj.Cells(x, y).Value
					if isinstance(one_value, float):
						rounded_value = round(one_value, input_no)
						sheet_obj.Cells(x, y).Value = rounded_value

	def run_vba_module(self, macro_name):
		"""
		텍스트로 만든 매크로 코드를 실행하는 코드이다

		:param macro_name: (str) 입력으로 들어오는 텍스트, 매크로이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.run_vba_module(macro_name="name1")
			<object_name>.run_vba_module("name1")
		"""
		self.xlapp.Run(macro_name)

	def save(self, input_filename):
		"""
		엑셀화일을 저장하는것

		:param input_filename: (str) 화일의 이름을 나타내는 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.save(input_filename="D:\\temp\\abc.xlsx")
			<object_name>.save("D:\\temp\\abc.xlsx")
			<object_name>.save("D:\\temp\\abc123.xlsx")
		"""
		if input_filename == "":
			self.xlbook.Save()
		else:
			self.xlbook.SaveAs(input_filename, 51)

	def screen_updating_off(self):
		self.xlapp.ScreenUpdating = True
		self.xlapp.Calculation = -4105

	def screen_updating_on(self):
		self.xlapp.ScreenUpdating = False
		self.xlapp.Calculation = -4135

	def scrollbar_for_sheet(self, sheet_name, xyxy):
		"""
		엑셀의 시트에 스크롤바의 형태를 설정하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_scrollbar_for_sheet(sheet_name="", xyxy="")
			<object_name>.set_scrollbar_for_sheet("sht1", [1,1,3,20])
			<object_name>.set_scrollbar_for_sheet("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		pxywh = self.xyxy2_to_pxywh(sheet_name, xyxy)
		scrollbar_obj = sheet_obj.Shapes.AddFormControl(Type=8, Left=pxywh[0], Top=pxywh[1], Width=pxywh[2],
															 Height=pxywh[3])
		scrollbar_obj.Name = "abc_1"
		scrollbar_obj.ControlFormat.Value = 4
		scrollbar_obj.ControlFormat.Min = 0
		scrollbar_obj.ControlFormat.Max = 359
		scrollbar_obj.ControlFormat.SmallChange = 1
		scrollbar_obj.ControlFormat.LargeChange = 10
		scrollbar_obj.ControlFormat.LinkedCell = "$A$1"

	def search_nth_continious_value(self, input_value, line_no):
		"""
		넘어온 자료중 line_no번째의 연속된 자료가 같은 갯수를 세어서 리스트형태로 돌려주는것

		:param input_value: (any) 입력값
		:param line_no: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.search_nth_continious_value(input_value="입력1", line_no=3)
			<object_name>.search_nth_continious_value("입력4", 3)
			<object_name>.search_nth_continious_value("입력5", 7)
		"""
		result = []
		num = 1
		for no in range(len(input_value) - 1):
			if input_value[no][line_no] == input_value[no + 1][line_no]:
				# 위와 아래의 Item이 같은것일때
				num = num + 1
			else:
				result.append(num)
				num = 1
		return result

	def search_password_for_unlock_sheet(self, num_tf="yes", text_small_tf="yes", text_big_tf="yes", special_tf="no", len_num=10):
		"""
		엑셀시트의 암호를 풀기위해 암호를 계속 만들어서 확인하는 것
		메뉴에서 제외

		:param num_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:param text_small_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:param text_big_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:param special_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:param len_num: (int) 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.search_password_for_unlock_sheet(num_tf="yes", text_small_tf="yes", text_big_tf="yes", special_tf="no", len_num=10)
			<object_name>.search_password_for_unlock_sheet("yes", "yes", "yes", "no", 10)
			<object_name>.search_password_for_unlock_sheet(num_tf="yes", text_small_tf="no", text_big_tf="yes", special_tf="no", len_num=20)
		"""
		check_char = []
		if num_tf == "yes":
			check_char.extend(list(string.digits))
		if text_small_tf == "yes":
			check_char.extend(list(string.ascii_lowercase))
		if text_big_tf == "yes":
			check_char.extend(list(string.ascii_uppercase))
		if special_tf == "yes":
			for one in "!@#$%^*_-":
				check_char.extend(one)

		zz = itertools.combinations_with_replacement(check_char, len_num)
		for aa in zz:
			try:
				pswd = "".join(aa)
				self.set_sheet_lock_off("", pswd)
				break
			except:
				pass

	def search_sheet_hwnd(self, excel_hwnd):
		"""
		시트의 핸들값을 갖고오는 것

		:param excel_hwnd: (int) 핸들값, 엑셀의 핸들값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.search_sheet_hwnd(excel_hwnd=310834)
			<object_name>.search_sheet_hwnd(310834)
		"""
		child_windows = self.enum_child_windows(excel_hwnd)
		sheet_hwnd = None
		for child in child_windows:
			class_name = win32gui.GetClassName(child)
			if class_name == "EXCEL7":
				sheet_hwnd = child
				break
		return sheet_hwnd

	def search_value_by_xre_for_range_with_paint(self, sheet_name, xyxy, input_xre, color_name):
		"""
		영역의 값중에서 입력으로 들어온 xre형식의 정규표현식에 맞는 것이 있으면, 그 셀에 색칠하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_xre: (str) xre형식의 문자열
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.search_value_by_xre_for_range_with_paint(sheet_name="", xyxy="", input_xre="[영어:1~4][한글:3~10]", color_name="yel70")
			<object_name>.search_value_by_xre_for_range_with_paint("sht1", "", "[영어:1~4][한글:3~10]", color_name="yel70")
			<object_name>.search_value_by_xre_for_range_with_paint(sheet_name="", xyxy=[1,1,5,7], input_xre="[시작:처음][영어:1~4][한글:3~10]", color_name="yel70")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_obj.Cells(x, y).Value2
				found_or_not = self.rex.search_all_by_xsql(input_xre, str(one_value))
				if found_or_not:
					sheet_obj.Cells(x, y).Interior.Color = self.color.change_xcolor_to_rgbint(color_name)

	def search_value_by_xre_with_paint(self, input_xre, color_name):
		for x in range(self.x1, self.x2 + 1):
			for y in range(self.y1, self.y2 + 1):
				one_value = self.sheet_obj.Cells(x, y).Value2
				found_or_not = self.rex.search_all_by_xsql(input_xre, str(one_value))
				if found_or_not:
					self.sheet_obj.Cells(x, y).Interior.Color = self.color.change_xcolor_to_rgbint(color_name)

	def search_xre_for_selection_with_new_sheet(self, input_xre):
		"""
		엑셀의 현재 선택한 영역의 셀들을 적용한후에 새로운 시트에 그 결과를 나타내주는 것

		:param input_xre: (str) xre형식의 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.search_xre_for_selection_with_new_sheet(input_xre="[영어:1~4][한글:3~10]")
			<object_name>.search_xre_for_selection_with_new_sheet("[영어:1~4][한글:3~10]")
			<object_name>.search_xre_for_selection_with_new_sheet(input_xre="[시작:처음][영어:1~4][한글:3~10]")
		"""
		l2d = self.read_value_for_range("", "")
		result_l2d_1 = self.rex.match_for_l2d_by_xsql(input_xre, l2d)

		result_l2d = self.change_l2d_over_to_l2d(result_l2d_1)
		self.new_sheet()
		self.write_l2d_from_cell("", [1, 1], result_l2d)

	def select(self):
		self.range_obj.Select()

	def select_all(self, sheet_name):
		"""
		모든 영역을 선택한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_all(sheet_name="")
			<object_name>.select_all("sht1")
			<object_name>.select_all("")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.Cells.Select()

	def select_bottom_cell_for_range(self, sheet_name, xyxy):
		"""
		선택한 위치에서 제일왼쪽, 제일아래로 이동
		xlDown: - 4121,xlToLeft : - 4159, xlToRight: - 4161, xlUp : - 4162

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_cell_for_range_to_bottom(sheet_name="", xyxy="")
			<object_name>.select_cell_for_range_to_bottom("sht1", [1,1,3,20])
			<object_name>.select_cell_for_range_to_bottom("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.End(-4121).Select()

	def select_bottom_of_selection(self):
		self.range_obj.End(-4121).Select()

	def select_by_offset(self, oxyxy=""):
		"""
		현재의 셀 위치에서, offset으로 옮기는 것

		:param oxyxy: (list or str) [1,1,2,2], 가로세로셀영역을 나타내며, ""을 입력한 경우는 현재 선택영역을 나태냄
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_by_offset(oxyxy="")
			<object_name>.select_by_offset("")
			<object_name>.select_by_offset([1,1,1,20])
		"""
		sheet_obj = self.check_sheet_name("")
		x1, y1, x2, y2 = self.get_address_for_selection()
		ox1, oy1, ox2, oy2 = self.change_any_address_to_xyxy(oxyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1 + ox1, y1 + oy1), sheet_obj.Cells(x2 + ox2, y2 + oy2))
		range_obj.Select()

	def select_cell_by_xy_step(self):
		xyxy2 = self.get_address_for_activecell()
		self.sheet_obj.Cells(xyxy2[0] + self.x1, xyxy2[1] + self.y1).Select()

	def select_cell_for_range_by_xy_step(self, sheet_name, xyxy):
		"""
		activecell을 offset으로 이동시키는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_cell_for_range_by_xy_step(sheet_name="", xyxy="")
			<object_name>.select_cell_for_range_by_xy_step("sht1", [1,1,3,20])
			<object_name>.select_cell_for_range_by_xy_step("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		xyxy2 = self.read_address_for_activecell()
		sheet_obj.Cells(xyxy2[0] + x1, xyxy2[1] + y1).Select()

	def select_cells_for_sheet(self):
		self.sheet_obj.Cells.Select()

	def select_currentregion_for_cell(self):
		address_usedrange = self.get_address_for_currentregion()
		self.select_xyxy(address_usedrange)

	def select_currentregion_for_cell_for_range(self, sheet_name, xyxy):
		address_usedrange = self.get_address_for_currentregion(sheet_name, xyxy)
		self.select_range(sheet_name, address_usedrange)

	def select_for_cell(self, sheet_name, xyxy):
		"""
		셀을 활성화 하는것은 셀을 선택하는것과 같으며
		만약 영역이 들어오면 가장 왼쪽위의 영역을 선택합니다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_cell(sheet_name="", xyxy="")
			<object_name>.select_cell("sht1", [1,1,3,20])
			<object_name>.select_cell("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Select()

	def select_for_range(self, sheet_name, xyxy):
		"""
		영역을 선택한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_range_for_range(sheet_name="", xyxy="")
			<object_name>.select_range_for_range("sht1", [1,1,3,20])
			<object_name>.select_range_for_range("", "")
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Select()
		result = range_obj.Address
		return result

	def select_left_end(self):
		self.range_obj.End(-4159).Select()

	def select_left_end_cell_for_range(self, sheet_name, xyxy):
		"""
		입력값 : 입력값없이 사용가능
		선택한 위치에서 끝부분으로 이동하는것
		xlDown : - 4121, xlToLeft : - 4159, xlToRight : - 4161, xlUp : - 4162

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_cell_for_range_to_left_end(sheet_name="", xyxy="")
			<object_name>.select_cell_for_range_to_left_end("sht1", [1,1,3,20])
			<object_name>.select_cell_for_range_to_left_end("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.End(-4159).Select()

	def select_multi_range(self, input_range_list_l2d):
		input_range_list_l2d = self.util.change_any_data_to_l2d(input_range_list_l2d)

		[self.x1, self.y1, self.x2, self.y2] = self.change_any_address_to_xyxy(input_range_list_l2d[0])
		multi_range = self.new_range_obj()

		if len(input_range_list_l2d) > 1:
			for index, one_range in enumerate(input_range_list_l2d[1:]):
				self.change_any_address_to_xyxy(one_range)
				range_2 = self.new_range_obj()

				multi_range = self.xlapp.Union(multi_range, range_2)
		multi_range.Select()

	def select_multi_range_for_sheet(self, sheet_name, input_range_list_l2d):
		"""
		영역을 선택한다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_multi_range(sheet_name="", input_range_list_l2d=[[1,1, 3,5], [13,24], [37,48]])
			<object_name>.select_multi_range("", [[1,1, 3,5], [13,24], [37,48]])
			<object_name>.select_multi_range("sht1", input_range_list_l2d=[[1,1, 3,5], [13,24], [37,48]])
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		input_range_list_l2d = self.util.change_any_data_to_l2d(input_range_list_l2d)

		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(input_range_list_l2d[0])
		multi_range = self.new_range_obj(sheet_name, [x1, y1, x2, y2])

		if len(input_range_list_l2d) > 1:
			for index, one_range in enumerate(input_range_list_l2d[1:]):
				self.change_any_address_to_xyxy(one_range)
				range_2 = self.new_range_obj(sheet_name, [x1, y1, x2, y2])

				multi_range = self.xlapp.Union(multi_range, range_2)
		multi_range.Select()

	def select_range_for_range_name(self, input_range_list_l2d):
		self.select_range_name(input_range_list_l2d)

	def select_range_for_xxline(self, sheet_name, xx_list):
		self.select_xxline(sheet_name, xx_list)

	def select_range_for_yyline(self, sheet_name, yy_list):
		self.select_yyline(sheet_name, yy_list)

	def select_range_name(self, input_range_list_l2d):
		"""
		여러 영역을 선택하는 방법
		이것은 이름영역의 주소형태를 다루는 것이다
		sheet_xyxy_list = [["시트이름1", [1,1,4,4]], ["시트이름2", []], ]

		:param input_range_list_l2d: (list) 2차원의 list형 자료, 2차원의 형태로 여러영역을 나타내며, 시트이름도 포함을 해서 2차원의 자료이다
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_range_name(sheet_name="", input_range_list_l2d=[[1,1, 3,5], [13,24], [37,48]])
			<object_name>.select_range_name("", [[1,1, 3,5], [13,24], [37,48]])
			<object_name>.select_range_name("sht1", input_range_list_l2d=[[1,1, 3,5], [13,24], [37,48]])
		"""

		uninput_range = []

		if not isinstance(input_range_list_l2d, list):
			input_range_list_l2d = [input_range_list_l2d]

		for one_named_range in input_range_list_l2d:
			all_address, sheet, xyxy = self.get_address_name(one_named_range)

			sheet_obj = self.check_sheet_name(sheet)
			x1, y1, x2, y2 = xyxy
			r1c1 = self.xyxy2_to_r1c1([x1, y1, x2, y2])
			range_obj = sheet_obj.Range(r1c1)
			if uninput_range == []:
				uninput_range = range_obj
				check_name = sheet
			else:
				if check_name == sheet:
					uninput_range = self.xlapp.Union(uninput_range, range_obj)
				else:
					uninput_range.Select()
					sheet_obj.Select()
					uninput_range = range_obj
					check_name = sheet
			uninput_range.Select()

	def select_right_end_cell_for_range(self, sheet_name, xyxy):
		"""
		선택한 위치에서 끝부분으로 이동하는것
		xlDown: - 4121,xlToLeft : - 4159, xlToRight: - 4161, xlUp : - 4162

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_cell_for_range_to_right_end(sheet_name="", xyxy="")
			<object_name>.select_cell_for_range_to_right_end("sht1", [1,1,3,20])
			<object_name>.select_cell_for_range_to_right_end("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.End(-4161).Select()

	def select_right_end_of_selection(self):
		self.range_obj.End(-4161).Select()

	def select_sheet(self, sheet_name):
		"""
		시트이름으로 시트를 선택

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_sheet(sheet_name="")
			<object_name>.select_sheet("sht1")
			<object_name>.select_sheet("")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.Select()

	def select_top_cell_for_range(self, sheet_name, xyxy):
		"""
		선택한 위치에서 끝부분으로 이동하는것
		xlDown: - 4121,xlToLeft : - 4159, xlToRight: - 4161, xlUp : - 4162

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_cell_for_range_to_top(sheet_name="", xyxy="")
			<object_name>.select_cell_for_range_to_top("sht1", [1,1,3,20])
			<object_name>.select_cell_for_range_to_top("", [1,9,6,87])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.End(-4162).Select()

	def select_top_end_for_range(self, sheet_name, xyxy):
		"""
		영역의 제일 위로 이동

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_top_end_of_selection(sheet_name="", xyxy="")
			<object_name>.select_top_end_of_selection("sht1", [1,1,3,20])
			<object_name>.select_top_end_of_selection("", "")
		"""
		xldown = -4121
		xltoleft = -4159
		xltoright = -4161
		xlup = -4162

		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		for num in [xldown, xltoleft, xltoright, xlup]:
			range_obj.End(num).Select()
			aa = self.get_address_for_activecell()

	def select_top_line_for_range(self, sheet_name, xyxy):
		"""
		영역의 제일 위로 이동

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_top_line_for_range(sheet_name="", xyxy="")
			<object_name>.select_top_line_for_range("sht1", [1,1,3,20])
			<object_name>.select_top_line_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		sheet_obj.Cells(x1, y1).Select()

	def select_top_line_of_selection(self):
		self.sheet_obj.Cells(self.x1, self.y1).Select()

	def select_top_of_selection(self):
		xldown = -4121
		xltoleft = -4159
		xltoright = -4161
		xlup = -4162

		for num in [xldown, xltoleft, xltoright, xlup]:
			self.range_obj.End(num).Select()
			aa = self.get_address_for_activecell()

	def select_usedrange(self):
		address_usedrange = self.get_address_for_usedrange('')
		self.select_xyxy(address_usedrange)

	def select_usedrange_for_sheet(self, sheet_name):
		"""
		활성화된 시트의 사용역역인 usedrange를 선택하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_usedrange(sheet_name="")
			<object_name>.select_usedrange("sht1")
			<object_name>.select_usedrange("")
		"""
		address_usedrange = self.get_address_for_usedrange(sheet_name)
		self.select_range(sheet_name, address_usedrange)

	def select_workbook(self, input_filename):
		"""
		열려진 워드 화일중 이름으로 선택하는것

		:param input_filename: (str) 화일의 이름을 나타내는 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_workbook(input_filename="D:\\temp\\abc.xlsx")
			<object_name>.select_workbook("D:\\temp\\abc.xlsx")
			<object_name>.select_workbook("D:\\temp\\abc123.xlsx")
		"""
		self.xlapp.Visible = True
		win32gui.SetForegroundWindow(self.xlapp.hwnd)
		self.xlapp.Workbooks(input_filename).Activate()
		self.xlapp.WindowState = win32com.client.constants.xlMaximized

	def select_xline_for_sheet(self, sheet_name, x_list):
		"""
		하나의 가로줄을 선택하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param x_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_xline(sheet_name="", x_list=[2,4,6])
			<object_name>.select_xline("", [1,3,20])
			<object_name>.select_xline("", [1,20])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		if isinstance(x_list, int):
			x_list = [x_list]

		start = self.change_char_to_num(x_list[0])
		changed_address = str(start) + ":" + str(start)
		sheet_obj.Rows(changed_address).Select()

	def select_xxline(self, xx_list):

		start = self.change_char_to_num(xx_list[0])
		end = self.change_char_to_num(xx_list[1])
		changed_address = str(start) + ":" + str(end)
		range_obj = self.sheet_obj.Rows(changed_address).Select()

	def select_xxline_for_sheet(self, sheet_name, xx_list):
		"""
		연속된 가로줄을 선택하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xx_list: (list) 가로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_xxline(sheet_name="", xx_list=[3,5])
			<object_name>.select_xxline("", [1,3])
			<object_name>.select_xxline("", [1,20])
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		start = self.change_char_to_num(xx_list[0])
		end = self.change_char_to_num(xx_list[1])
		changed_address = str(start) + ":" + str(end)
		range_obj = sheet_obj.Rows(changed_address).Select()

	def select_xyxy(self):
		self.range_obj.Select()
		result = self.range_obj.Address
		return result

	def select_yline_for_sheet(self, sheet_name, y_list):
		"""
		하나의 세로열을 선택하는 것
		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param y_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_yline(sheet_name="", y_list=[2,4,6])
			<object_name>.select_yline("", [1,3,20])
			<object_name>.select_yline("", [1,20])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		if isinstance(y_list, int):
			y_list = [y_list]

		start = self.change_num_to_char(y_list[0])
		changed_address = str(start) + ":" + str(start)
		sheet_obj.Columns(changed_address).Select()

	def select_yyline(self, yy_list):
		start = self.change_num_to_char(yy_list[0])
		end = self.change_num_to_char(yy_list[1])

		changed_address = str(start) + ":" + str(end)
		self.sheet_obj.Columns(changed_address).Select()

	def select_yyline_for_sheet(self, sheet_name, yy_list):
		"""
		연속된 세로열을 선택하는 것
		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param yy_list: (list) 세로줄의 사작과 끝 => [3,7]
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.select_yyline(sheet_name="", yy_list=[2, 4])
			<object_name>.select_yyline("", [2, 4])
			<object_name>.select_yyline("sht1", [3,7])
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		start = self.change_num_to_char(yy_list[0])
		end = self.change_num_to_char(yy_list[1])

		changed_address = str(start) + ":" + str(end)
		sheet_obj.Columns(changed_address).Select()

	def selection(self):
		"""
		선택영역의 객체를 돌려주는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.selection()
		"""
		range_obj = self.xlapp.Selection
		return range_obj

	def set_alert_off(self):
		"""
		경고문이 나오고 안나오게 만드는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.setup_alert_off()
		"""
		self.xlapp.DisplayAlerts = False

	def set_alert_on(self):
		"""
		알람을 보여줄지를 설정하는것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.setup_alert_on()
		"""
		self.xlapp.DisplayAlerts = True

	def set_auto_next_line_for_range(self, sheet_name, xyxy, input_value):
		"""
		셀안에 들어가는 값이 셀영역을 넘어갈때 다음줄로 줄바꿈을 적용할것인지를 설정하는것
		만약 status를 false로 하면 줄바꿈이 실행되지 않는다.

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_auto_next_line_for_range(sheet_name="", xyxy="", input_value="입력값")
			<object_name>.set_auto_next_line_for_range("", "", "입력값")
			<object_name>.set_auto_next_line_for_range(sheet_name="sht1", xyxy=[1,1,7,10], input_value="입력값")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		range_obj.WrapText = input_value

	def set_border_line_color(self, color_name):
		self.varx["border_line"]["color_int"] = self.color.change_any_color_to_rgbint(color_name)

	def set_border_line_style(self, *input_list):
		# 내부적으로 들어오는 형태가 튜플로 2차원까지 문제가 될소지가 있어 변경하는 부분이다
		self.varx["line_color"] = 0
		self.varx["line_style"] = 1
		self.varx["line_thicness"] = 1
		self.varx["line_position"] = [1]

		# 위의 4가지를 잘 선택하면 되는 것이다
		if isinstance(input_list, list) and isinstance(input_list[0], list) and len(input_list) == 1:
			input_list = input_list[0]
		for one in input_list:
			print("색발견 =>", one)
			if one in list(self.varx["check_line_thickness"].keys()):
				self.varx["line_thicness"] = self.varx["check_line_thickness"][one]
			elif one in list(self.varx["line_style_vs_enum"].keys()):
				self.varx["line_style"] = self.varx["line_style_vs_enum"][one]
			elif one in list(self.varx["check_line_position"].keys()):
				self.varx["line_position"] = self.varx["check_line_position"][one]
			elif isinstance(one, int):
				self.varx["line_position"].append(one)
			else:
				try:
					self.varx["line_color"] = self.color.change_xcolor_to_rgbint(one)
				except:
					pass

	def draw_border_line(self):
		for po_no in self.varx["line_position"]:
			self.range_obj.Borders(po_no).Color = self.varx["line_color"]
			self.range_obj.Borders(po_no).Weight = self.varx["line_thicness"]
			self.range_obj.Borders(po_no).LineStyle = self.varx["line_style"]



	def set_border_line_thickness(self, thickness):
		self.varx["border_line"]["thickness"] = self.varx["check_line_thickness"][thickness]

	def font_for_range(self, sheet_name, xyxy, *input_list):
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		if isinstance(input_list[0], list):
			input_list = input_list[0]

		for one in input_list:
			if one in ["진하게", "굵게", "찐하게", "bold"]:				range_obj.Font.Bold = True
			elif one in ["italic", "이태리", "이태리체", "기울기"]:			range_obj.Font.Italic = True
			elif one in ["strikethrough", "취소선", "통과선", "strike"]:	range_obj.Font.Strikethrough = True
			elif one in ["subscript", "하위첨자", "밑첨자"]:				range_obj.Font.Superscript = True
			elif one in ["superscript", "위첨자", "웃첨자"]:				range_obj.Font.Subscript = True
			elif one in ["underline", "밑줄"]:							range_obj.Font.Underline = True
			elif isinstance(one, int):									range_obj.Font.Size = one
			else:
				try:
					range_obj.Font.Color = self.color.change_xcolor_to_rgbint(one)
				except:
					pass

	def set_font(self, *input_list):

		if isinstance(input_list[0], list):
			input_list = input_list[0]

		for one in input_list:
			if one in ["진하게", "굵게", "찐하게", "bold"]:
				self.range_obj.Font.Bold = True
			elif one in ["italic", "이태리", "이태리체", "기울기"]:
				self.range_obj.Font.Italic = True
			elif one in ["strikethrough", "취소선", "통과선", "strike"]:
				self.range_obj.Font.Strikethrough = True
			elif one in ["subscript", "하위첨자", "밑첨자"]:
				self.range_obj.Font.Superscript = True
			elif one in ["superscript", "위첨자", "웃첨자"]:
				self.range_obj.Font.Subscript = True
			elif one in ["underline", "밑줄"]:
				self.range_obj.Font.Underline = True
			elif isinstance(one, int):
				self.range_obj.Font.Size = one
			else:
				try:
					self.range_obj.Font.Color = self.color.change_xcolor_to_rgbint(one)
				except:
					pass


	def font_as_dic(self, *input_list):
		self.setup_font_basic()

		if isinstance(input_list[0], list):
			input_list = input_list[0]

		for one in input_list:
			if one in ["진하게", "굵게", "찐하게", "bold"]: self.varx["font"]["bold"] = True
			elif one in ["italic", "이태리", "이태리체", "기울기"]:	self.varx["font"]["italic"] = True
			elif one in ["strikethrough", "취소선", "통과선", "strike"]: self.varx["font"]["strikethrough"] = True
			elif one in ["subscript", "하위첨자", "밑첨자"]: self.varx["font"]["subscript"] = True
			elif one in ["superscript", "위첨자", "웃첨자"]: self.varx["font"]["superscript"] = True
			elif one in ["underline", "밑줄"]: 	self.varx["font"]["underline"] = True
			elif isinstance(one, int):		self.varx["font"]["size"] = one
			else:
				try:
					self.varx["font"]["color"] = self.color.change_xcolor_to_rgbint(one)
				except:
					pass
		return


	def set_font_as_dic(self, input_list):
		"""
		여러번 사용이 가능하도록 내가 원하는 폰트에 대한 설정을 저장해서 return값으로 돌려받는 다
		["진하게", 12, "red50", "밑줄"] 이런형식으로 들어오면 알아서 값이 되는 것이다

		:param input_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_font(input_list=[1, "abc", "가나다"])
			<object_name>.set_font([1, "abc", "가나다"])
			<object_name>.set_font([1, "abc", "가나다"])
		"""
		self.setup_font_basic()

		if isinstance(input_list[0], list):
			input_list = input_list[0]

		for one in input_list:
			if one in ["진하게", "굵게", "찐하게", "bold"]: self.varx["font"]["bold"] = True
			if one in ["italic", "이태리", "이태리체", "기울기"]: self.varx["font"]["italic"] = True
			if one in ["strikethrough", "취소선", "통과선", "strike"]: self.varx["font"]["strikethrough"] = True
			if one in ["subscript", "하위첨자", "밑첨자"]: self.varx["font"]["subscript"] = True
			if one in ["superscript", "위첨자", "웃첨자"]: self.varx["font"]["superscript"] = True
			if one in ["underline", "밑줄"]: self.varx["font"]["underline"] = True
			if one in ["vertical", "수직", "가운데"]: self.varx["font"]["align_v"] = 3
			if one in ["horizental", "수평", "중간"]: self.varx["font"]["align_h"] = 2

			try:
				self.varx["font"]["size"] = int(one)
			except:
				pass

			try:
				result = self.rex.search_all_by_xsql("[한글&영어:1~]", one)
				if result:
					if result[0][0] in self.varx["check_color_name"]:
						self.varx["font"]["color"] = self.color.change_xcolor_to_rgbint(one)
			except:
				pass
		result = copy.deepcopy(self.varx["font"])

		return result

	def set_font_basic(self):
		"""
		폰트에대한 기본 정보를 만드는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_font_basic()
		"""
		# 기본값을 만들고, 다음에 이것을 실행하면 다시 기본값으로 돌아온다

		# 폰트 설정의 모든것을 초기화 하는것
		#self.varx["font"]["background"] = None
		#self.varx["font"]["colorindex"] = 1
		#self.varx["font"]["creator"] = None
		#self.varx["font"]["style"] = None
		#self.varx["font"]["themecolor"] = None
		#self.varx["font"]["themefont"] = None
		#self.varx["font"]["tintandshade"] = None
		self.varx["font"]["bold"] = False
		self.varx["font"]["italic"] = False
		self.varx["font"]["name"] = "Arial"
		self.varx["font"]["size"] = 12
		self.varx["font"]["strikethrough"] = False
		self.varx["font"]["subscript"] = False
		self.varx["font"]["superscript"] = False
		#self.varx["font"]["alpha"] = False  # tintandshade를 이해하기 쉽게 사용하는 목적
		self.varx["font"]["underline"] = False
		self.varx["font"]["align_v"] = 2  # middle =3, top = 1, bottom = 4, default=2
		self.varx["font"]["align_h"] = 1  # None =1, center=2, left=1, default=1
		self.varx["font"]["color"] = 1

	def set_formats_for_target_line(self, input_shape_obj):
		"""
		선택된 도형객체에 공통변수들을 할당하는 것

		:param input_shape_obj: (object) 객체, 도형객체
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_formats_for_target_line(input_shape_obj="shape1")
			<object_name>.set_formats_for_target_line("shape1")
		"""
		input_shape_obj.DashStyle = self.varx["pen_style"]
		input_shape_obj.ForeColor.RGB = self.varx["pen_color"]
		input_shape_obj.Weight = self.varx["pen_thickness"]
		input_shape_obj.BeginArrowheadLength = self.varx["start_point_length"]
		input_shape_obj.BeginArrowheadStyle = self.varx["start_point_style"]
		input_shape_obj.BeginArrowheadWidth = self.varx["start_point_width"]
		input_shape_obj.EndArrowheadLength = self.varx["end_point_length"]
		input_shape_obj.EndArrowheadStyle = self.varx["end_point_style"]
		input_shape_obj.EndArrowheadWidth = self.varx["end_point_width"]

	def set_formula(self, input_value):
		self.range_obj.Formula = input_value

	def set_gradation_for_color_n_position(self, in_style, in_obj, color_name, input_l2d):
		"""
		여러 가지색을 정하면서, 색의 가장 진한 위치를 0~100 사이에서 정하는 것
		self.setup_gradation_for_color_n_position("hor", aaa, "blu++", ["red++++", 0])

		:param in_style: (str) 안쪽색의 스타일을 나타내는 문자열
		:param in_obj: (object) 객체,
		:param color_name: (str) 색이름을 나타내는 표현으로 red56, 빨강56
		:param input_l2d: (list) 2차원의 리스트
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_gradation_for_color_n_position(in_style="center", in_obj="object1", color_name="red50", input_l2d=[[1, 2], [4, 5]])
			<object_name>.set_gradation_for_color_n_position("center", "object1", "red50", [[1, 2], [4, 5]])
			<object_name>.set_gradation_for_color_n_position("center", "object7", color_name="red45", input_l2d=[[1, 2], [4, 5]])
		"""
		input_l2d = self.check_input_data(input_l2d)
		style_dic = {"ver": 2, "hor": 1, "corner": 5, "center": 7, "down": 4, "up": 3, "mix": -2}
		in_obj.Fill.ForeColor.RGB = self.color.change_xcolor_to_rgbint(color_name)
		obj_fill = in_obj.Fill
		obj_fill.OneColorGradient(style_dic[in_style], 1, 1)
		for index, l1d in enumerate(input_l2d):
			rgbint = self.color.change_xcolor_to_rgbint(l1d[0])
			obj_fill.GradientStops.Insert(rgbint, l1d[1] / 100)

	def set_height(self, height_float):
		self.range_obj.RowHeight = height_float

	def set_hide(self, xx_list):
		self.x1, self.x2 = self.check_xx_address(xx_list)
		self.sheet_obj.Rows(str(self.x1) + ":" + str(self.x2)).Hidden = True

	def find_value(self, old_word, start_cell, value_or_fomular, part_or_whole_tf, direction, direction_next, case_tf,
				   byte_type_tf,  cell_format_tf):

		self.range_obj.Find(old_word, old_word, start_cell, value_or_fomular, part_or_whole_tf, direction,
							direction_next, case_tf,
							byte_type_tf, cell_format_tf)

	def replace_value(self, old_word, new_word, part_or_whole_tf, direction, case_tf, byte_type_tf, cell_format_tf,
					  replace_cell_format_tf):

		self.range_obj.Replace(old_word, new_word, part_or_whole_tf, direction, case_tf, byte_type_tf, cell_format_tf,
							   replace_cell_format_tf)

	def set_interactive_off(self):
		"""
		자료가 변경이되면 차트등이 연결되서 실행되는것을 interactive라고 한다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_interactive_off()
		"""

		self.xlapp.Interactive = False

	def set_interactive_on(self):
		"""
		자료가 변경이되면 차트등이 연결되서 실행되는것을 interactive라고 한다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_interactive_on()
		"""
		self.xlapp.Interactive = True

	def set_invisible_for_workbook(self, visible_tf=1):
		"""
		실행되어있는 엑셀을 화면에 보이지 않도록 설정합니다
		기본설정은 보이는 것으로 되너 있읍니다

		:param visible_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_invisible_for_workbook(visible_tf=1)
			<object_name>.set_invisible_for_workbook(1)
			<object_name>.set_invisible_for_workbook(False)
		"""
		self.xlapp.Visible = 0

	def set_maxmized_for_screen(self):
		"""
		엑셀화일을 최대화합니다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_maxmized_for_screen()
		"""
		self.xlapp.WindowState = -4137

	def set_minimized_for_screen(self):
		"""
		엑셀화일을 최소화합니다

		xlMaximized : -4137
		xlMinimized : -4140
		xlNormal : -4143

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_minimized_for_screen()
		"""
		self.xlapp.WindowState = -4140

	def set_numberformat(self, input_yno, style):
		if style == 1:  # 날짜의 설정
			self.sheet_obj.Columns(input_yno).NumberFormatLocal = "mm/dd/yy"
		elif style == 2:  # 숫자의 설정
			self.sheet_obj.Columns(input_yno).NumberFormatLocal = "_-* #,##0.00_-;-* #,##0.00_-;_-* '-'_-;_-@_-"
		elif style == 3:  # 문자의 설정
			self.sheet_obj.Columns(input_yno).NumberFormatLocal = "@"

	def set_numberformat_for_column(self, sheet_name, input_yno=5, style="style1"):
		"""
		각 열을 기준으로 셀의 속성을 설정하는 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_yno: (int) 정수, 엑셀의 세로열(column) 번호를 나타내는것
		:param style: (str) 입력으로 들어오는 텍스트, 모양을 나타내는 스타일을 넣는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_numberformat_in_column(sheet_name="", input_yno=1, type1='general')
			<object_name>.set_numberformat_in_column(sheet_name="", input_yno=4, type1='number')
			<object_name>.set_numberformat_in_column(sheet_name="", input_yno=7, type1='date')
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		if style == 1:  # 날짜의 설정
			sheet_obj.Columns(input_yno).NumberFormatLocal = "mm/dd/yy"
		elif style == 2:  # 숫자의 설정
			sheet_obj.Columns(input_yno).NumberFormatLocal = "_-* #,##0.00_-;-* #,##0.00_-;_-* '-'_-;_-@_-"
		elif style == 3:  # 문자의 설정
			sheet_obj.Columns(input_yno).NumberFormatLocal = "@"

	def find_value_for_range(self, sheet_name, xyxy, old_word="old1", start_cell=[3, 5], value_or_fomular=3, part_or_whole_tf=False, direction=1, direction_next=1, case_tf=False,
							byte_type_tf=False,
							cell_format_tf=False):
		"""
		엑셀의 찾기 바꾸기 기능을 이용하는 것
		만약 * 또는 ? 기호가 포함된 데이터를 찾거나 수식에 포함하고 싶다면 해당 문자 앞에 ~(물결표)를 붙여주면 됩니다.
		찾기를 하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param old_word: 찾고싶은 문자열, 필수 검색할 문자열	 문자열이나 숫자 같은 모든 데이터 유형
		:param start_cell: (list) 시작 셀, 검색을 시작할 셀 셀 주소
		:param value_or_fomular: 값인지 수식인지를 선택하는 것, 검색에 수식, 값, 코맨트 사용 xlValues, xlFormulas, xlComments
		:param part_or_whole_tf: (bool) 선택사항	부분일치 또는 전체 일치 xlWhole, xlPart
		:param direction: 앞으로 찾을것인지 찾는 방향을 선택 하는 것, 검색할 순서 – 행 또는 열	 xlByRows, xlByColummns
		:param direction_next: (str) 선택사항	검색할 방향 – 순방향 또는 역방향	 xlNext, xlPrevious
		:param case_tf: (bool) 대소문자, 대소문자 구분 여부 True 또는 False
		:param byte_type_tf: (bool) 더블 바이트 문자 지원을 설치한 경우에만 사용(예: 중국어) True 또는 False
		:param cell_format_tf: (bool) 선택사항, 셀 서식으로 검색 허용 True 또는 False
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.find_value_for_range(sheet_name="", xyxy="", old_word="old1", start_cell=[3,5], value_or_fomular=3, part_or_whole=False, direction=1, direction_next=1, case=False, byte_type=False, cell_format=False)
			<object_name>.find_value_for_range("", "", "old1", [3,5], 3, False, 1, 1, False, False, False)
			<object_name>.find_value_for_range(sheet_name="sht1", xyxy=[1,1,3,4], old_word="old1", start_cell=[3,5], value_or_fomular=3, part_or_whole=False, direction=1, direction_next=1, case=False, byte_type=False, cell_format=False)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Find(old_word, old_word, start_cell, value_or_fomular, part_or_whole_tf, direction,
					   direction_next, case_tf,
					   byte_type_tf, cell_format_tf)

	def replace_value_for_range(self, sheet_name, xyxy, old_word="abc1", new_word="ddd1", part_or_whole_tf=False, direction=1, case_tf=False, byte_type_tf=False, cell_format_tf=False,
							   replace_cell_format_tf=False):
		"""
		만약 * 또는 ? 기호가 포함된 데이터를 찾거나 수식에 포함하고 싶다면 해당 문자 앞에 ~(물결표)를 붙여주면 됩니다.
		바꾸기를 하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param old_word: (str) 찾고싶은 문자열, 필수 검색할 문자열	 문자열이나 숫자 같은 모든 데이터 유형
		:param new_word: (str) 바꿀 문자열
		:param part_or_whole_tf: (bool) 선택사항	부분일치 또는 전체 일치 xlWhole, xlPart
		:param direction: 앞으로 찾을것인지 찾는 방향을 선택 하는 것, 검색할 순서 – 행 또는 열	 xlByRows, xlByColummns
		:param case_tf: (bool) 대소문자, 대소문자 구분 여부 True 또는 False
		:param byte_type_tf: (bool) 더블 바이트 문자 지원을 설치한 경우에만 사용(예: 중국어) True 또는 False
		:param cell_format_tf: (bool) 선택사항, 셀 서식으로 검색 허용 True 또는 False
		:param replace_cell_format_tf:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.replace_value_for_range(sheet_name="", xyxy="", old_word="abc1", new_word="ddd1", part_or_whole_tf=False, direction=1, case_tf=False, byte_type_tf=False, cell_format_tf=False, replace_cell_format_tf=False)
			<object_name>.replace_value_for_range("", "", "abc1", "ddd1", False, 1, False, False, False, False)
			<object_name>.replace_value_for_range(sheet_name="sht1", xyxy=[1,1,3,5], old_word="abc1", new_word="ddd1", part_or_whole_tf=False, direction=1, case_tf=False, byte_type_tf=False, cell_format_tf=False, replace_cell_format_tf=False)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Replace(old_word, new_word, part_or_whole_tf, direction, case_tf, byte_type_tf, cell_format_tf,
						  replace_cell_format_tf)

	def set_numberproperty(self, type1):
		if type1 == 'general' or type1 == '':
			result = "#,##0.00_ "
		elif type1 == 'number':
			result = "US$""#,##0.00"
		elif type1 == 'account':
			result = "_-""US$""* #,##0.00_ ;_-""US$""* -#,##0.00 ;_-""US$""* ""-""??_ ;_-@_ "
		elif type1 == 'date':
			result = "mm""/""dd""/""xx"
		elif type1 == 'datetime':
			result = "xxxx""-""m""-""d h:mm AM/PM"
		elif type1 == 'percent':
			result = "0.00%"
		elif type1 == 'bunsu':
			result = "# ?/?"
		elif type1 == 'jisu':
			result = "0.00E+00"
		elif type1 == 'text':
			result = "@"
		elif type1 == 'etc':
			result = "000-000"
		elif type1 == 'other':
			result = "$#,##0.00_);[빨강]($#,##0.00)"
		else:
			result = type1  # 만약 아무것도 해당이 않된다면, 그냥 사용자가 서식을 정의한 것이다

		r1c1 = self.xyxy2_to_r1c1([self.x1, self.y1, self.x2, self.y2])
		range_obj = self.sheet_obj.Range(r1c1)
		self.range_obj.NumberFormat = result

	def set_password(self, password):
		self.set_sheet_lock(password)

	def set_pattern(self, input_list):
		input_list = self.check_input_data(input_list)

		self.setup_basic_data()
		if input_list:
			# 아무것도 없으면, 기존의 값을 사용하고, 있으면 새로이 만든다
			if isinstance(input_list, list):
				self.set_font(input_list)
			elif isinstance(input_list, dict):
				# 만약 사전 형식이면, 기존에 저장된 자료로 생각하고 update한다
				self.varx["pattern"].update(input_list)
		a = 2
		if a == 1:
			self.range_obj.Interior.Color = 5296274
			self.range_obj.Interior.Pattern = self.varx["range_color"]["pattern"]
			self.range_obj.Interior.PatternColor = self.varx["range_color"]["pattern"]

		elif a == 2:
			self.range_obj.Interior.Gradient.Degree = 180
			self.range_obj.Interior.Gradient.ColorStops.Clear()
			self.range_obj.Interior.Gradient.ColorStops.Add(0)

		elif a == 3:
			self.range_obj.Interior.Color = 5296274
			self.range_obj.Interior.Pattern = self.varx["range_color"]["pattern"]  # xlSolid
			self.range_obj.Interior.PatternColor = self.varx["range_color"][
				"pattern"]  # PatternColorIndex = xlAutomatic
			self.range_obj.Interior.ThemeColor = 4  # xlThemeColorDark1 색상과 색조를 미리 설정한것을 불러다가 사용하는것
			# 이것은 기본적으로 마우스의 색을 선택할때 나타나는 테마색을 말하는 것이다

			self.range_obj.Interior.TintAndShade = -0.249977111117893  # 명암을 조절
			self.range_obj.Interior.PatternTintAndShade = 0

		return self.varx["range_color"]

	def set_range(self, xyxy):
		"""
			작업의 대상이 되는 시트와 영역을 인스턴스 변수(self.sheet_obj, self.range_obj)에 설정함

			:param sheet_name: (str) 시트 이름, ""은 현재 활성화된 시트
			:param xyxy: (list or str) 영역 주소 (예: "A1:B3" 또는 [r1, c1, r2, c2])
			:return: None
			"""
		if self.sheet_obj == None:
			self.set_sheet("")
		[self.x1, self.y1, self.x2, self.y2] = self.change_any_address_to_xyxy(xyxy)
		self.range_obj = self.sheet_obj.Range(self.sheet_obj.Cells(self.x1, self.y1),
											  self.sheet_obj.Cells(self.x2, self.y2))

	def set_range_by_activecell_xline(self, no):
		xy = self.get_address_for_activecell()
		self.x1 = xy[0]
		self.x2 = xy[2]
		self.range_obj = self.sheet_obj.Rows(self.x1 + ':' + self.x2)

	def set_range_by_range_name(self, input_name):
		self.xlbook.Names.Add(input_name, self.range_obj)

	def set_range_by_selection(self):
		temp_address = self.xlapp.Selection.Address
		temp_address = temp_address.split(",")  # 여러곳을 선택했는지 확인하기 위한것
		result = self.change_any_address_to_xyxy(temp_address[0])

	def set_range_by_usedrange(self):
		self.change_any_address_to_xyxy(self.sheet_obj.UsedRange.Address)

	def set_range_for_xline_no(self, input_no):
		self.x = input_no
		self.y = None

	def set_range_for_xxline(self, *input_list):
		self.x1 = self.change_char_to_num(input_list[0])
		if len(input_list) > 1:
			self.x2 = self.change_char_to_num(input_list[1])
		else:
			self.x2 = self.x1
		self.range_obj = self.sheet_obj.Rows(self.x1 + ':' + self.x2)

	def set_range_for_yline_no(self, input_no):
		self.x = None
		self.y = input_no

	def set_range_for_yyline(self, *input_list):
		self.y1 = self.change_num_to_char(input_list[0])
		if len(input_list) > 1:
			self.y2 = self.change_num_to_char(input_list[1])
		else:
			self.y2 = self.y1
		self.range_obj = self.sheet_obj.Columns(self.y1 + ':' + self.y2)

	def set_screen_update_off(self):
		"""
		화면 변화를 잠시 멈추는것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_screen_update_off()
		"""
		self.xlapp.ScreenUpdating = False

	def set_screen_update_on(self):
		"""
		화면이 빠귀는 기준에 대해서 매번 바꾸리때마다 화면을 udate하도록 설정하는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_screen_update_on()
		"""
		self.xlapp.ScreenUpdating = True

	def set_scrollbar(self):
		pxywh = self.xyxy2_to_pxywh("")
		scrollbar_obj = self.sheet_obj.Shapes.AddFormControl(Type=8, Left=pxywh[0], Top=pxywh[1], Width=pxywh[2], Height=pxywh[3])
		scrollbar_obj.Name = "abc_1"
		scrollbar_obj.ControlFormat.Value = 4
		scrollbar_obj.ControlFormat.Min = 0
		scrollbar_obj.ControlFormat.Max = 359
		scrollbar_obj.ControlFormat.SmallChange = 1
		scrollbar_obj.ControlFormat.LargeChange = 10
		scrollbar_obj.ControlFormat.LinkedCell = "$A$1"

	def set_sheet(self, sheet_name=None):
		self.sheet_obj = self.check_sheet_name(sheet_name)

	def set_value(self, value):
		self.value = self.util.change_any_type_to_l2d(value)

	def set_visible_for_sheet(self, input_tf=0):
		"""
		실행되어있는 엑셀을 화면에 보이지 않도록 설정합니다
		기본설정은 보이는 것으로 되너 있읍니다

		:param input_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_visible_for_sheet(input_tf=0)
			<object_name>.set_visible_for_sheet(1)])
			<object_name>.set_visible_for_sheet(0)])
		"""
		self.xlapp.Visible = input_tf

	def set_visible_for_workbook(self, input_tf=1):
		"""
		실행되어있는 엑셀을 화면에 보이지 않도록 설정합니다
		기본설정은 보이는 것으로 되너 있읍니다

		:param value: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_visible_for_workbook(input_tf=1)
			<object_name>.set_visible_for_workbook(1)
			<object_name>.set_visible_for_workbook(input_tf=0)
		"""
		self.xlapp.Visible = input_tf

	def set_width(self, width):
		self.range_obj.ColumnWidth = width

	def set_wrap_for_range(self, sheet_name, xyxy, input_value):
		"""
		셀안의 값이 여러줄일때 줄바꿈이 되도록 설정하는 것
		줄바꿈이 가능하도록 설정하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_wrap_for_range(sheet_name="", xyxy="", input_value="입력 텍스트")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.WrapText = input_value

	def set_wraptext(self, input_tf=True):
		self.range_obj.WrapText = input_tf

	def set_x1(self, input_x1):
		self.x1 = self.x1 + input_x1

	def set_x2(self, input_x2):
		self.x2 = self.x2 + input_x2

	def set_xy(self, *input_xy):
		if len(input_xy) ==1:
			input_xy = input_xy[0]
		self.x1 = input_xy[0]
		self.y1 = input_xy[1]

	def set_y1(self, input_y1):
		self.y1 = self.y1 + input_y1

	def set_y2(self, input_y2):
		self.y2 = self.y2 + input_y2

	def shape_degree(self, input_shape_obj, degree):
		input_shape_obj.IncrementRotation(degree)

	def shape_degree_for_sheet(self, sheet_name, input_shape_obj, degree):
		"""
		도형을 회전시키는 것
		도형은 중간을 기준으로 회=전을 합니다
		shape _ obi :이동시킬 도형 이름

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_shape_obj: (object) 객체, 도형 객체
		:param degree:
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.shape_degree(sheet_name="", input_shape_obj="object1", degree=45)
			<object_name>.shape_degree("", "object1", 35)
			<object_name>.shape_degree(sheet_name="sht1", input_shape_obj="object4", degree=55)
		"""
		input_shape_obj.IncrementRotation(degree)

	def shape_font(self, input_dic):
		"""
		도형의 폰트를 설정하는 것

		:param input_dic: (dic) 사전형으로 입력되는 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_font_for_shape(input_dic = {"key1":1, "line_1":"red", "input_color":"red", "font_bold":1})
			<object_name>.set_font_for_shape({"key1":1, "line_1":"red", "input_color":"red", "font_bold":1})
			<object_name>.set_font_for_shape(input_dic = {"key1":1, "line_2":"red", "input_color1":"red", "font_bold1":1}])
		"""
		if "color" in input_dic.keys():
			input_dic["color"] = self.color.change_xcolor_to_rgbint(input_dic["color"])
		self.varx["shape_font"].update(input_dic)
		return self.varx["shape_font"]

	def shape_line_head(self, head_style, head_h, head_w):
		"""
		선택영역에서 선을 긋는것
		선긋기를 좀더 상세하게 사용할수 있도록 만든것
		밐의 base_data의 값들을 이용해서 입력하면 된다

		:param head_style:(int) 라인의 head 스타일 번호
		:param head_h: (int) 라인의 head를 나타내는 높이
		:param head_w: (int) 라인의 head를 나타내는 넓이
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_line_head_for_shape(tail_style=1, tail_h=10, tail_w=30)
			<object_name>.set_line_head_for_shape(tail_style=2, tail_h=12, tail_w=35)
			<object_name>.set_line_head_for_shape(tail_style=3, tail_h=10, tail_w=40)
		"""
		enum_line = self.varx["end_style_vs_enum"]
		base_data = self.varx["dic_base_cell_data"]
		self.varx["setup"]["line"]["head_style"] = enum_line[base_data["head_style"]]
		self.varx["setup"]["line"]["head_h"] = enum_line[base_data["head_h"]]
		self.varx["setup"]["line"]["head_w"] = enum_line[base_data["head_w"]]

	def shape_line_tail(self, tail_style, tail_h, tail_w):
		"""
		선택영역에서 선을 긋는것
		선긋기를 좀더 상세하게 사용할수 있도록 만든것
		밐의 base_data의 값들을 이용해서 입력하면 된다

		:param tail_style: (int) 라인의 tail 스타일 번호
		:param tail_h: (int) 라인의 tail를 나타내는 높이
		:param tail_w: (int) 라인의 tail를 나타내는 넓이
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_line_tail_for_shape(tail_style=1, tail_h=10, tail_w=30)
			<object_name>.set_line_tail_for_shape(tail_style=2, tail_h=12, tail_w=35)
			<object_name>.set_line_tail_for_shape(tail_style=3, tail_h=10, tail_w=40)
		"""
		enum_line = self.varx["end_style_vs_enum"]
		base_data = self.varx["dic_base_cell_data"]
		self.varx["setup"]["line"]["tail_style"] = enum_line[base_data["tail_style"]]
		self.varx["setup"]["line"]["tail_h"] = enum_line[base_data["tail_h"]]
		self.varx["setup"]["line"]["tail_w"] = enum_line[base_data["tail_w"]]

	def shape_ratio_in_sheet(self, sheet_name, shape_name="name1", wh_connect_tf=True):
		"""
		사진의 비율변경을 해제하거나 설정하는 목적
		Selection.ShapeRange.LockAspectRatio = msoTrue

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param shape_name: (str) 입력으로 들어오는 텍스트, 도형이나 그림객체의 이름
		:param wh_connect_tf: (bool) 변경시 기존 비율대로 적용할것인지를 설정하는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_ratio_for_shape(sheet_name="", shape_name="name1", wh_connect_tf=True)
			<object_name>.set_ratio_for_shape("", "name1", True)
			<object_name>.set_ratio_for_shape(sheet_name="sht1", shape_name="name1", wh_connect_tf=True)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		input_shape_obj = sheet_obj.Shapes(shape_name)
		input_shape_obj.LockAspectRatio = wh_connect_tf

	def shape_size(self, shape_no, width_float, height_float, lock_ratio_tf):
		input_shape_obj = self.sheet_obj.Shapes(shape_no)
		if lock_ratio_tf:
			input_shape_obj.LockAspectRatio = True
		else:
			input_shape_obj.LockAspectRatio = False
		# 도형의 크기 조정
		input_shape_obj.Width = width_float
		input_shape_obj.Height = height_float

	def shape_size_for_sheet(self, sheet_name, shape_no, width_float=12.3, height_float=8.9, lock_ratio_tf=True):
		"""
		도형(이미지포함)의 크기를 변경시키는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param shape_no: (int) 정수, 도형의 번호
		:param width_float: (int) 넓이를 나타내는 정수
		:param height_float: (int) 높이를 나타내는 정수
		:param lock_ratio_tf: (bool) 크기변경시 기존 비율을 그대로 변경할것인지 설정
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_size_for_shape(sheet_name="", shape_no=10, width_float=12.3, height_float=8.8, lock_ratio=True)
			<object_name>.set_size_for_shape("", 12.3, 8.8, True)
			<object_name>.set_size_for_shape(sheet_name="sht1", shape_no=20, width_float=12.3, height_float=8.8, lock_ratio=True)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		input_shape_obj = sheet_obj.Shapes(shape_no)
		if lock_ratio_tf:
			input_shape_obj.LockAspectRatio = True
		else:
			input_shape_obj.LockAspectRatio = False
		# 도형의 크기 조정
		input_shape_obj.Width = width_float
		input_shape_obj.Height = height_float

	def sheet_lock(self, sheet_name, password="1234"):
		"""
		입력받은 암호를 사용해서 시트를 잠그기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param password: (str) 입력으로 들어오는 텍스트, 암호를 나타내는 문자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_sheet_lock(sheet_name="", password="1234")
			<object_name>.set_sheet_lock("", "암호1")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.protect(password)

	def shft_x(self, input_no):
		self.x1 = self.x1 + input_no

	def shft_y(self, input_no):
		self.y1 = self.y1 + input_no

	def show_excel_data_at_webbrower_with_datatables(self, xyxy, input_filename):
		"""
		엑셀자료의 형태는
		[x좌표, y좌표, 설명, 분류] 또는
		[한글주소, "", 설명, 분류] 또는

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_filename: (str) 화일의 이름을 나타내는 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.show_excel_data_at_webbrower_with_datatables(xyxy="", input_filename="D:\\temp\\abc.xlsx")
			<object_name>.show_excel_data_at_webbrower_with_datatables("", "D:\\temp\\abc.xlsx")
			<object_name>.show_excel_data_at_webbrower_with_datatables("sht1", "D:\\temp\\abc.xlsx")
		"""

		if not input_filename.endswith(".html"): input_filename = input_filename + ".html"

		json_code, title_list, input_filename = self.xyxy2_to_json_file("", xyxy="", input_filename="D:\\temp\\abc.xlsx")

		aaa = """
			<!DOCTYPE html>
			<html lang="kr"><head><meta charset="UTF-8">
			<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
			<script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
			<link href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.min.css" rel="stylesheet"/>

			<script>
			var data=""" + json_code + """;
			$(document).ready(function() {
			$('#product-inventory-level').DataTable( {
				"data": data,
				"columns": [
			"""
		bbb = ""
		for one in title_list:
			bbb = bbb + '{ "data": "' + one + '"},'

		ccc = """ ], }); });
			</script>
			<title></title>
			</head><body><table id="product-inventory-level" class="display" style="width:100%"><thead><tr>"""

		ddd = ""
		for one in title_list:
			ddd = ddd + '<th>' + one + '</th>'
		eee = """</tr></thead></table></body></html>"""

		total_code = aaa + bbb + ccc + ddd + eee

		self.show_html_code_at_webbrowser(total_code, input_filename)

	def show_file_dialog(self):
		"""
		화일 다이얼로그를 불러오는 것

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.show_file_dialog()
		"""
		filter = "Picture Files \0*.jp*;*.gif;*.bmp;*.png\0Text files\0*.txt\0"
		# filter = "Picture Files (*.jp*; *.gif; *.bmp; *.png),*.xls"
		# win32con.OFN_EXPLORER : 0x00080000
		# win32con.OFN_ALLOWMULTISELECT : 0x00000200

		result = win32gui.GetOpenFileNameW(InitialDir=os.environ["temp"],
										   Filter=filter, Flags=0x00000200 | 0x00080000,
										   File="somefilename", DefExt="py",
										   Title="GetOpenFileNameW", FilterIndex=0)
		return result

	def show_html_code_at_webbrowser(self, input_html_code, input_filename):
		"""
		html코드를 화일이아닌 코드 자체를 갖고와서 웹브라우져로 여는 것
		결론적으로는 화일을 만드는것과 같은것 같다
		엑셀의 자료를 datatables를 이용하여 테이블 형식으로 웹브라유져에 나타내는 코드임

		:param input_html_code: (str) html형식의 문자열
		:param input_filename: (str) 화일의 이름을 나타내는 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.show_html_code_at_webbrowser(input_html_code=code1, input_filename="D:\\temp\\abc.xlsx")
			<object_name>.show_html_code_at_webbrowser(code1, "D:\\temp\\abc.xlsx")
			<object_name>.show_html_code_at_webbrowser(input_html_code=code7, input_filename="D:\\temp\\abc.xlsx")
		"""
		f = open(input_filename, 'w', encoding="utf-8")
		f.write(input_html_code)
		f.close()
		webbrowser.open_new_tab('file:///' + os.getcwd() + '/' + input_filename)

	def sort_2_excel_files_001(self):
		"""
		두개시트의 자료를 기준으로 정렬한다선택한
		단 두개의 자료는 각각 정렬이되어있어야 한다
		빈칸은 없어야 한다

		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.sort_2_excel_files_001()
		"""
		# 1. 두개의 시트의 첫번째 열을 읽어온다
		sheet_names = self.get_sheet_names()

		# 첫번째 시트의 첫번째 행의 자료를 갖고오는 것이다
		sheet1_name = sheet_names[0]
		y_start, x_start, y_end, x_end = self.get_address_for_usedrange(sheet1_name)
		datas1 = self.read_value_for_range(sheet1_name, [1, x_start, 1, x_end])

		# 두번째 시트의 첫번째 행의 자료를 갖고오는 것이다
		sheet2_name = sheet_names[1]
		y_start, x_start, y_end, x_end = self.get_address_for_usedrange(sheet2_name)
		datas2 = self.read_value_for_range(sheet2_name, [1, x_start, 1, x_end])

		# 첫번째것과 두번째것을 비교하여 컬럼을 추가한다
		all_dic = {}
		for data1 in datas1:
			if data1[0] in all_dic:
				all_dic[data1[0]] = all_dic[data1[0]] + 1
			else:
				all_dic[data1[0]] = 1

		for data2 in datas2:
			if data2[0] in all_dic:
				all_dic[data2[0]] = all_dic[data2[0]] + 1
			else:
				all_dic[data2[0]] = 1

		# 각각 시트를 돌아가며 칸을 넣는다
		# 딕셔너리의 키를 리스트로 만든다
		all_dic_list = list(all_dic.keys())

		try:
			all_dic_list.remove(None)
		except:
			pass

		all_dic_list_sorted = sorted(all_dic_list)

		# 딕셔너리의 값들을 리스트로 만들어서 값을 만든다
		all_dic_values_list = list(all_dic.values())
		temp_1 = 0
		for one in all_dic_values_list:
			temp_1 = temp_1 + int(one)

		# 첫번째 시트를 맞도록 칸을 넣는다
		temp_2 = []
		for one in all_dic_list_sorted:
			for two in range(int(all_dic.get(one))):
				temp_2.append(one)

		temp_3 = 0
		for one in range(len(temp_2)):
			try:
				if temp_2[one] == datas1[temp_3][0]:
					temp_3 = temp_3 + 1
				else:
					self.insert_xxline(sheet1_name, one + 1)
			except:
				self.insert_xxline(sheet1_name, one + 1)

		temp_4 = 0
		for one in range(len(temp_2)):
			try:
				if temp_2[one] == datas2[temp_4][0]:
					temp_4 = temp_4 + 1
				else:
					self.insert_xxline(sheet2_name, one + 1)
			except:
				self.insert_xxline(sheet2_name, one + 1)

	def sort_with_two_range(self, sheet_name, xyxy1, xyxy2):
		"""
		두가지 영역을 정렬 하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy1: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param xyxy2: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.sort_with_two_range(sheet_name="", xyxy1=[1,1,30,30], xyxy2=[40,1, 70, 30])
			<object_name>.sort_with_two_range("", [1,1,30,30], [40,1, 70, 30])
			<object_name>.sort_with_two_range(sheet_name="sht1", xyxy1=[1,1,30,30], xyxy2=[40,1, 70, 30])
		"""
		l2d_1 = self.read_value_for_range(sheet_name, xyxy1)
		l2d_2 = self.read_value_for_range(sheet_name, xyxy2)
		l2d_3 = list(l2d_2)
		self.new_sheet()
		line = 1
		len_width = len(l2d_1[0])
		total_line_no = 1
		current_x = 0

		for index, one in enumerate(l2d_1):
			current_x = current_x + 1
			self.write_value_for_range("", [current_x, 1], one)
			temp = 0
			for index2, one_2 in enumerate(l2d_2):
				if one[0] == one_2[0] and (one[0] != "" or one[0] != None):
					temp = temp + 1
					if temp > 1:
						current_x = current_x + 1
					self.write_value_for_range("", [current_x, len_width + 1], one_2)
					l2d_3[index2] = ["", ""]

		total_line_no = line + len(l2d_1)
		for one in l2d_3:
			if one[0] != "" and one[0] != None:
				current_x = current_x + 1
				self.write_value_for_range("", [current_x, len_width + 1], one)

	def split_filename_to_path_n_filename(self, input_filename):
		"""
		화일 이름을 경로와 이름으로 구분하는 것이다

		:param filename: (str) 화일의 이름을 나타내는 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.split_filename_to_path_n_filename(input_filename="D:\\temp\\abc.xlsx")
			<object_name>.split_filename_to_path_n_filename("D:\\temp\\abc.xlsx")
			<object_name>.split_filename_to_path_n_filename("D:\\temp\\abc123.xlsx")
		"""
		path = ""
		changed_filename = input_filename.replace("\\", "/")
		split_list = changed_filename.split("/")
		filename_only = split_list[-1]
		if len(changed_filename) == len(filename_only):
			path = ""
		else:
			path = changed_filename[:len(filename_only)]

		return [path, filename_only]

	def split_l2d_value_by_special_char(self, input_l2d, split_char):
		"""
		2차원자료안의 모든 값을 특정문자로 분리하는 기능

		:param input_l2d: (list) 2차원의 list형 자료
		:param split_char: (str) 분리할 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.split_all_l2d_value_by_special_char(input_l2d=[[1, 2], [4, 5]], split_char="_")
			<object_name>.split_all_l2d_value_by_special_char([[1, 2], [4, 5]], "_")
			<object_name>.split_all_l2d_value_by_special_char(input_l2d=[[4,5,6],[7,8,9]], split_char=","])
		"""
		input_l2d = self.check_input_data(input_l2d)

		result = []
		for ix, l1d in enumerate(input_l2d):
			temp = ""
			for iy, value in enumerate(l1d):
				value = input_l2d[ix][iy]
				# value = self.read_value_for_cell("", [ix + 1, iy + 1])
				if isinstance(value, str):
					splited_value = value.split(split_char)
					if isinstance(splited_value, list):
						result.append(splited_value)
					else:
						result.append([splited_value])
				else:
					result.append([value])
		return result

	def split_partial_value_by_step_from_start(self, input_no):
		l2d = self.read()
		result = set()
		for l1d in l2d:
			for one in l1d:
				try:
					result.add(one[0:input_no])
				except:
					pass
		return list(result)

	def split_partial_value_for_range_by_step_from_start(self, sheet_name, xyxy, input_no):
		"""
		어떤 자료중에 앞에서 몇번째것들만 갖고오고 싶을때
		예:시군구 자료에서 앞의 2글자만 분리해서 얻어오는 코드

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_no: (int) 정수 글자를 나태내는 숫자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.split_partial_value_for_range_by_step_from_start(sheet_name="", xyxy="", input_no=7)
			<object_name>.split_partial_value_for_range_by_step_from_start("", "", 7)
			<object_name>.split_partial_value_for_range_by_step_from_start(sheet_name="sht1", xyxy="", input_no=7)
		"""
		l2d = self.read_value_for_range(sheet_name, xyxy)
		result = set()
		for l1d in l2d:
			for one in l1d:
				try:
					result.add(one[0:input_no])
				except:
					pass
		return list(result)

	def split_range_as_head_body_tail(self, xyxy, head_height, tail_height):
		"""
		테이블 형식의 영역을 head, body, tail 로 구분하는 것

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param head_height: (int) 정수, 높이를 나타내는 숫자
		:param tail_height: (int) 정수, 높이를 나타내는 숫자
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.split_range_as_head_body_tail(xyxy="", head_height=10, tail_height=10)
			<object_name>.split_range_as_head_body_tail("", 10, 10)
			<object_name>.split_range_as_head_body_tail("sht1", 15, 35)
		"""
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_head = [x1, y1, x1 + head_height - 1, y2]
		range_body = [x1 + head_height, y1, x2 - tail_height, y2]
		range_tail = [x2 - tail_height - 1, y1, x2, y2]
		return [range_head, range_body, range_tail]

	def split_text_by_special_string(self, input_value):
		# sheet_name = self.get_activesheet_name()
		rng_select = self.get_address_for_usedrange('')
		rng_used = self.get_address_for_usedrange('')
		[self.x1, self.y1, self.x2, self.y2] = self.intersect_range1_range2(rng_select, rng_used)
		self.insert_yyline("", self.y1 + 1)
		self.insert_yyline("", self.y1 + 1)
		result = []
		length = 2
		# 자료를 분리하여 리스트에 집어 넣는다
		for x in range(self.x1, self.x2 + 1):
			for y in range(self.y1, self.y2 + 1):
				one_value = str(self.sheet_obj.Cells(x, y).Value)
				list_data = one_value.split(input_value)
				result.append(list_data)
		# 집어넣은 자료를 다시 새로운 세로줄에 넣는다
		for x_no in range(len(result)):
			if len(result[x_no]) > length:
				for a in range(len(result[x_no]) - length):
					self.insert_yyline("", self.y1 + length)
				length = len(result[x_no])
			for y_no in range(len(result[x_no])):
				self.sheet_obj.Cells(self.x1 + x_no, self.y1 + y_no + 1).Value = result[x_no][y_no]

	def split_text_by_special_string_for_range(self, sheet_name, input_value):
		"""
		선택한 1줄의 영역에서 원하는 문자나 글자를 기준으로 분리할때
		2개의 세로행을 추가해서 결과값을 쓴다

		:param input_value: (str) 입력으로 들어오는 텍스트
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.split_text_by_special_string(input_value="입력글자1")
			<object_name>.split_text_by_special_string("입력문자들")
			<object_name>.split_text_by_special_string("입력으로 들어오는 문자")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		rng_select = self.read_selection_address()
		rng_used = self.read_usedrange_address()
		[x1, y1, x2, y2] = self.intersect_range1_range2(rng_select, rng_used)
		self.insert_yy("", y1 + 1)
		self.insert_yy("", y1 + 1)
		result = []
		length = 2
		# 자료를 분리하여 리스트에 집어 넣는다
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = str(sheet_obj.Cells(x, y).Value)
				list_data = one_value.split(input_value)
				result.append(list_data)
		# 집어넣은 자료를 다시 새로운 세로줄에 넣는다
		for x_no in range(len(result)):
			if len(result[x_no]) > length:
				for a in range(len(result[x_no]) - length):
					self.insert_yy("", y1 + length)
				length = len(result[x_no])
			for y_no in range(len(result[x_no])):
				sheet_obj.Cells(x1 + x_no, y1 + y_no + 1).Value = result[x_no][y_no]

	def split_value_by_input_word_and_insert_splitted_data(self, sheet_name, xyxy, splitted_char=","):
		"""
		1줄의 값을 특정문자를 기준으로 분리한후
		분리된 갯수가 있으면, 1개이상일때는, 아래부분에 새로운 열을 추가한후에 값을 넣는것
		여러줄을 선택하여도, 제일 첫줄만 적용한다

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param splitted_char: (str) 입력으로 들어오는 텍스트, 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.split_value_by_input_word_and_insert_splitted_data(xyxy="", splitted_char=",")
			<object_name>.split_value_by_input_word_and_insert_splitted_data("", ",")
			<object_name>.split_value_by_input_word_and_insert_splitted_data("", "#")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		for no in range(xyxy[2], xyxy[0], -1):
			value = self.read_value_for_cell("", [no, xyxy[1]])
			splited_value = value.split(splitted_char)
			sheet_obj.Cells(no, xyxy[1]).Value = splited_value[0].strip()
			if len(splited_value) > 1:
				for index, one in enumerate(splited_value[1:]):
					self.insert_xline("", no + index + 1)
					sheet_obj.Cells(no + index + 1, xyxy[1]).Value = one.strip()

	def split_xline_as_per_input_word_for_yline(self, sheet_name, xyxy, yline_index=2, input_value="입력텍스트", first_line_is_title_tf=True):
		"""
		선택한 영역에서 특정 y값이 입력값을 갖고있을때, 입력값들에 따라서 x라인들을 저장한후 돌려준다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param yline_index: (int) 정수
		:param input_value: (any) 입력값
		:param first_line_is_title_tf: (bool) 숫자일때는 false를 문자일때는 true를 넣는다
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.split_xline_as_per_input_word_for_yline(sheet_name="", xyxy="", yline_index=2, input_value="입력텍스트", first_line_is_title_tf=True)
			<object_name>.split_xline_as_per_input_word_for_yline("", "", 4, "입력텍스트", True)
			<object_name>.split_xline_as_per_input_word_for_yline(sheet_name="sht1", xyxy=[1,1,5,7], yline_index=2, input_value="입력텍스트", first_line_is_title_tf=True)
		"""
		l2d = self.read_value_for_range(sheet_name, xyxy)
		result = {"_main_data": []}
		for one_value in input_value:
			result[one_value] = []

		if first_line_is_title_tf:
			for one_key in result.keys():
				result[one_key].append(l2d[0])
			l2d = l2d[1:]

		for l1d in l2d:
			found = False
			for one_key in result.keys():
				if one_key in l1d[int(yline_index)]:
					result[one_key].append(l1d)
					found = True
			if found == False:
				result["_main_data"].append(l1d)

		return result

	def split_xre_for_selection_with_new_sheet(self, input_xre):
		"""
		선택영역안의 값에서 입력으로 들어온 xre형식의 정규표현식에 맞는것을
		새로운 시트에 써주는 것이다
		발견한것을 기준으로 원래 값을 분리하는것

		:param input_xre: (str) xre형식의 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.split_xre_for_selection_with_new_sheet(input_xre="[영어:1~4][한글:3~10]")
			<object_name>.split_xre_for_selection_with_new_sheet("[영어:1~4][한글:3~10]")
			<object_name>.split_xre_for_selection_with_new_sheet(input_xre="[시작:처음][영어:1~4][한글:3~10]")
		"""
		sheet_obj = self.check_sheet_name("")
		result = []
		xyxy = self.get_address_for_selection()
		for x in range(xyxy[0], xyxy[2] + 1):
			for y in range(xyxy[1], xyxy[3] + 1):
				one_value = sheet_obj.Cells(x, y).Value
				aaa = self.rex.search_all_by_xsql(input_xre, one_value)
				atemp = []
				if aaa:
					for num in range(len(aaa) - 1, -1, -1):
						one = aaa[num]
						no = one[2]
						temp = one_value[no:]
						one_value = one_value[:no]
						atemp.append(temp)
						atemp.insert(0, one_value)
				result.append(atemp)
		self.new_sheet()
		self.write_l2d_from_cell("", [1, 1], result)

	def to_capital(self):
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = self.sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				self.sheet_obj.Cells(x, y).Value = one_value.capitalize()

	def to_lower(self):
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = self.sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				self.sheet_obj.Cells(x, y).Value = one_value.lower()

	def to_ltrim(self):
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = self.sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				self.sheet_obj.Cells(x, y).Value = one_value.lstrip()

	def to_reverse(self):

		l2d = self.value
		changed_l2d = []
		for y in range(len(l2d[0])):
			temp = []
			for x in range(len(l2d)):
				temp.append(l2d[x][y])
			changed_l2d.append(temp)
		self.value = changed_l2d
		return self.value

	def to_rtrim(self):
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = self.sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				self.sheet_obj.Cells(x, y).Value = one_value.rstrip()

	def to_swapcase(self):
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = self.sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				self.sheet_obj.Cells(x, y).Value = one_value.swapcase()

	def to_text(self):
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = self.sheet_obj.Cells(x, y).Value
			if isinstance(one_value, (int, float)):
				self.sheet_obj.Cells(x, y).Value = str(one_value)

	def to_trim(self):
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = self.sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				self.sheet_obj.Cells(x, y).Value = one_value.strip()

	def to_upper(self):
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			one_value = self.sheet_obj.Cells(x, y).Value
			if isinstance(one_value, str):
				self.sheet_obj.Cells(x, y).Value = one_value.upper()

	def to_xyxy(self):

		temp = self.get_address_for_range_name(self.range_obj)
		xyxy = self.change_any_address_to_xyxy(temp[2])
		return xyxy

	def unhide_sheet_all(self):
		for sheet in self.xlbook.Sheets:
			# 시트의 Visible 속성을 -1 (xlSheetVisible)로 설정
			# -1: xlSheetVisible (보임)
			# 0: xlSheetHidden (숨김)
			# 2: xlSheetVeryHidden (매우 숨김)

			# 현재 시트의 Visible 상태를 확인하고 변경
			if sheet.Visible != -1:
				sheet.Visible = -1  # 보이도록 설정

	def unmerge(self):
		self.range_obj.UnMerge()

	def unmerge_for_range(self, sheet_name, xyxy):
		"""
		입력영역안에 병합된 것이 있으면 병합을 해제하기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.unmerge_for_range(sheet_name="", xyxy="")
			<object_name>.unmerge_for_range("sht1", [1,1,3,20])
			<object_name>.unmerge_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.UnMerge()

	def vlookup_for_multi_input(self, sheet_name, xyxy, search_no_list, search_value_list, find_no, option_all=True):
		"""
		여러 값이 같은 줄을 갖고오는 방법

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param search_no_list: (list) 찾을 가로줄의 번호들
		:param search_value_list: (list) 찾을 값을 리스트형태로 만든것
		:param find_no: (int) 몇개까지 같은것을 찾아야하는지 설정하는 것
		:param option_all: (bool) option을 선택하는것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.vlookup_for_multi_input(sheet_name="", xyxy="", search_no_list=[1, 3, 5], search_value_list=["abc","가나다"], find_no=3, option_all=True)
			<object_name>.vlookup_for_multi_input("", "", [1, 3, 5], ["abc","가나다"], find_no=3, option_all=True)
			<object_name>.vlookup_for_multi_input(sheet_name="sht1", xyxy=[1,1,3,7], search_no_list=[1, 3, 5], search_value_list=["abc","가나다"], find_no=3, option_all=True)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		result = []
		l2d = self.read_value_for_range(sheet_name, xyxy)
		checked_no = len(search_value_list)

		for l1d in l2d:
			temp_no = 0
			for index, num in enumerate(search_no_list):
				if option_all:
					# 모든 값이 다 같을때
					if l1d[num - 1] == search_value_list[index]:
						temp_no = temp_no + 1
					else:
						break
				else:
					# 값이 일부분일때도 OK
					if search_value_list[index] in l1d[num - 1]:
						temp_no = temp_no + 1
					else:
						break
			if temp_no == checked_no:
				result = l1d[find_no - 1]
		return result

	def vlookup_for_range(self, sheet_name, find_xyxy="", check_xyxy="", find_value_option="top", find_value_oxy=[2, 4], write_value_oxy=[3, 4]):
		"""
		영역에 vlookup을 적용

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param find_xyxy: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param check_xyxy: (list or str) 주소값의 형태, 보통 [1,1,2,2]의형태, ""은 현재 선택영역이며, (xyxy : [왼쪽 위 row번호,왼쪽 위 col번호, 오른쪽 아래 row번호,오른쪽 아래 col번호])
		:param find_value_option: (str)
		:param find_value_oxy: (list) 찾을값이 있는 셀의 위치
		:param write_value_oxy: (list) 찾은값을 쓰기위한 위치
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.vlookup_xyxy(sheet_name="", find_xyxy="", check_xyxy="", find_value_option="top", find_value_oxy=[2, 4], write_value_oxy=[3,4])
			<object_name>.vlookup_xyxy("", "", "", "top", [2, 4], [3,4])
			<object_name>.vlookup_xyxy(sheet_name="sht1", find_xyxy="", check_xyxy="", find_value_option="top", find_value_oxy=[2, 4], write_value_oxy=[3,4])
		"""
		sheet_obj = self.check_sheet_name("")
		original_l2d = self.read_value_for_range(sheet_name, find_xyxy)
		dic_data = self.read_as_dic_with_xy_position(sheet_name, find_xyxy)

		l2d = self.read_value_for_range(sheet_name, check_xyxy)

		for ix, l1d in enumerate(l2d):
			for iy, one_value in enumerate(l1d):
				if one_value in dic_data.keys():
					find_x, find_y = dic_data[one_value][0]

				if find_value_option == "top":
					change_x = 0
					change_y = find_y - 1
				else:
					change_x = find_x - 1 + find_value_oxy[0]
					change_y = find_y - 1 + find_value_oxy[1]
				write_value = original_l2d[change_x][change_y]
				write_x = check_xyxy[0] + write_value[0] + ix
				write_y = check_xyxy[1] + write_value[1] + iy
				sheet_obj.Cells(write_x, write_y).Value = write_x, write_y

	def vlookup_with_multi_input_line(self, input_value1, input_value2):
		"""
		보통 vlookup은 한줄을 비교해서 다른 자료를 찾는데
		이것은 여러항목이 같은 값을 기준으로 원하는 것을 찾는 것이다
		input_valuel = [자료의영역, 같은것이있는위치, 결과값의위치]

		:param input_value1: (any) 입력값
		:param input_value2: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.vlookup_with_multi_input_line(input_value1="입력1", input_value2="입력2")
			<object_name>.vlookup_with_multi_input_line("입력1", "입력2")
			<object_name>.vlookup_with_multi_input_line(input_value1="입력12", input_value2="입력7")
		"""
		sheet_obj = self.check_sheet_name("")
		input_value1 = self.check_input_data(input_value1)
		input_value2 = self.check_input_data(input_value2)

		base_data2d = self.read_value_for_range("", input_value1[0])
		compare_data2d = self.read_value_for_range("", input_value2[0])
		result = ""
		for one_data_1 in base_data2d:
			gijun = []
			one_data_1 = list(one_data_1)
			for no in input_value1[1]:
				gijun.append(one_data_1[no - 1])
			x = 0

			for value_1d in compare_data2d:
				value_1d = list(value_1d)
				x = x + 1
				bikyo = []

				for no in input_value2[1]:
					bikyo.append(value_1d[no - 1])

				if gijun == bikyo:
					result = one_data_1[input_value1[2] - 1]
				sheet_obj.Cells(x, input_value2[2]).Value = result

	def vlookup_xyxy(self, find_xyxy, check_xyxy, find_value_option, find_value_oxy, write_value_oxy):
		original_l2d = self.read_value_for_range("", find_xyxy)
		dic_data = self.read_as_dic_with_xy_position(find_xyxy)

		l2d = self.read_value_for_range("", check_xyxy)

		for ix, l1d in enumerate(l2d):
			for iy, one_value in enumerate(l1d):
				if one_value in dic_data.keys():
					find_x, find_y = dic_data[one_value][0]

				if find_value_option == "top":
					change_x = 0
					change_y = find_y - 1
				else:
					change_x = find_x - 1 + find_value_oxy[0]
					change_y = find_y - 1 + find_value_oxy[1]
				write_value = original_l2d[change_x][change_y]
				write_x = check_xyxy + write_value[0] + ix
				write_y = check_xyxy + write_value[1] + iy
				self.sheet_obj.Cells(write_x, write_y).Value = write_x, write_y

	def width_for_yline_for_sheet(self, sheet_name, input_yno, height_float=13.5):
		"""
		가로열의 높이를 설정하는 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_yno: (int) 정수, 엑셀의 세로열(column) 번호를 나타내는것
		:param height_float: (int) 높이를 나타내는 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_width_for_yline(sheet_name="sht1", input_yno=3, height_float=13.5)
			<object_name>.set_width_for_yline(sheet_name="", input_yno=7, height_float=13.5)
			<object_name>.set_width_for_yline("", 9, 13.5)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		new_y = self.check_xy_address(input_yno)
		range_obj = sheet_obj.Range(sheet_obj.Cells(new_y[0], 1), sheet_obj.Cells(new_y[1], 5))
		range_obj.EntireRow.RowHeight = height_float

	def width_for_yyline_for_sheet(self, sheet_name, xyxy, width_float=13.5):
		"""
		입력영역의 세로의 넓이를 설정하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param width_float: (int) 넓이를 나타내는 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_width_for_yyline(self, sheet_name, xyxy, width_float=13.5)
			<object_name>.set_width_for_yyline("", "", 1,5)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.ColumnWidth = width_float

	def write(self, value, value_first=False):
		if self.sheet_obj == None: self.set_sheet("")
		if self.range_obj == None: self.set_range("")
		if value == None:
			l2d = self.value
		else:
			l2d = self.util.change_any_type_to_l2d(value)
		if value_first:
			# 최대의 갯수를 기준으로 나머지 항목들은 "을 추가한다
			may_y_len = max(len(row) for row in l2d)
			for row in l2d:
				row.extend([""] * (may_y_len - len(row)))
			self.sheet_obj.Range(self.sheet_obj.Cells(self.x1, self.y1),
								 self.sheet_obj.Cells(self.x1 + len(l2d) - 1, self.y1 + len(l2d[0]) - 1)).Value = l2d
		else:
			may_y_len = self.y2 - self.y1 + 1
			for row in l2d:
				current_len = len(row)
				if current_len < may_y_len:  # 부족한 경우: "" 추가
					row.extend([""] * (may_y_len - current_len))
				elif current_len > may_y_len:  # 많은 경우: 초과분 삭제
					del row[may_y_len:]
			self.sheet_obj.Range(self.sheet_obj.Cells(self.x1, self.y1),
								 self.sheet_obj.Cells(self.x2, self.y2)).Value = l2d

	def write_cell(self, input_value):
		self.sheet_obj.Cells(self.x1, self.y1).Value = input_value

	def write_cell_with_offset_for_range(self, sheet_name, xy, xy_offset, input_value):
		"""
		offset 으로 값을 쓸수있도록 만든것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함 기준이되는 셀의 위치
		:param xy_offset: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함 기준점에서 얼마나 떨어진 위치인지를 나타내 주는 것
		:param input_value: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_cell_with_offset(sheet_name="", xy=[2,2], xy_offset=[3,2], input_value="입력값")
			<object_name>.write_cell_with_offset("", [2,3], [3,1], "입력값")
			<object_name>.write_cell_with_offset("", [2,2], [0,2], "입력값")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xy)
		sheet_obj.Cells(x1 + xy_offset[0], y1 + xy_offset[1]).Value = input_value

	def write_df_to_excel(self, input_df, xy):
		"""
		df자료를 커럼과 값을 기준으로 나누어서 결과를 돌려주는 것이다

		:param input_df: dataframe객체
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_df_to_excel(input_df=df1, xy=[1,3])
			<object_name>.write_df_to_excel(df1, [1,3])
			<object_name>.write_df_to_excel(input_df=df22, xy=[11,13])
		"""
		col_list = input_df.columns.values.tolist()
		value_list = input_df.values.tolist()
		self.write_l1d_from_cell_as_yline("", xy, col_list)
		self.write_range_as_speedy("", [xy[0] + 1, xy[1]], value_list)

	def write_dic_for_range(self, sheet_name, xyxy, input_dic):
		"""
		사전으로 입력된 키값을 엑셀에 쓰는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_dic: (dic) 사전형으로 입력되는 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_key_n_value_of_dic_for_range(sheet_name="", xyxy="", input_dic={"key1":"value1", "key2":"값2"})
			<object_name>.write_key_n_value_of_dic_for_range("", "", {"key1":"value1", "key2":"값2"})
			<object_name>.write_key_n_value_of_dic_for_range(sheet_name="sht1", xyxy="", input_dic={"key1":"value1", "key2":"값2"})
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		l2d = list(input_dic.items())

		for x in range(len(l2d)):
			sheet_obj.Cells(x + x1, y1).Value = l2d[x][0]
			sheet_obj.Cells(x + x1, y1 + 1).Value = l2d[x][1]

	def write_empty_cell_for_range_as_uppercell_value(self, sheet_name, xyxy):
		"""
		영역에서 빈셀을 발견하면, 그 위의 있는 셀의 값으로 채우는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_uppercell_value_in_emptycell_for_range(sheet_name="", xyxy="")
			<object_name>.write_uppercell_value_in_emptycell_for_range("sht1", [1,1,3,20])
			<object_name>.write_uppercell_value_in_emptycell_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		l2d = self.read_value_for_range(sheet_name, xyxy)

		for y in range(len(l2d[0])):
			old_value = ""
			for x in range(len(l2d)):
				if l2d[x][y] == "" or l2d[x][y] == None:
					sheet_obj.Cells(x + x1, y + y1).Value = old_value
				else:
					old_value = l2d[x][y]

	def write_end_of_column(self, xy, input_l1d):
		self.select_bottom_of_selection(xy)
		xyxy = self.get_address_for_activecell()
		self.write([xyxy[0] + 1, xyxy[1]], input_l1d)

	def write_end_of_column_for_range(self, sheet_name, xy, input_l1d):
		"""
		a3을 예로들어서, a3을 기준으로, 입력한 값이있는제일 마지막 가로줄번호를 갖고온후,
		그 다음줄에 값을 넣는것
		어떤 선택된 자료의 맨 마지막에 값을 넣기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param input_l1d: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_value_at_end_of_column(sheet_name="", xy=[1,3], input_l1d=[1, "abc", "가나다"])
			<object_name>.write_value_at_end_of_column("", [1,3], [1, "abc", "가나다"])
			<object_name>.write_value_at_end_of_column(sheet_name="sht1", xy=[5,7], input_l1d=[17,"abc","가나다"])
		"""

		self.move_activecell_to_bottom(sheet_name, xy)
		xy = self.get_address_for_activecell()
		self.write_range(sheet_name, [xy[0] + 1, xy[1]], input_l1d)

	def write_excel_function_for_range(self, sheet_name, xy, input_fucntion="sum", xyxy=""):
		"""
		셀에 엑셀의 함수를 입력해 주는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param input_fucntion: (str) 입력으로 들어오는 텍스트, 함수의 이름
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_excel_function_for_cell(sheet_name="", xy=[2, 4], input_fucntion="sum", xyxy="")
			<object_name>.write_excel_function_for_cell("", [2, 4], "sum", "")
			<object_name>.write_excel_function_for_cell(sheet_name="sht1", xy=[2, 4], input_fucntion="sum", xyxy="")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		range = self.xyxy2_to_r1c1(xyxy)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xy)
		result = "=" + input_fucntion + "(" + range + ")"
		sheet_obj.Cells(x1, y1).Value = result

	def write_except_none(self, input_l2d):
		input_l2d = self.check_input_data(input_l2d)

		for ix, l1d in enumerate(input_l2d):
			for iy, one_value in enumerate(l1d):
				if one_value != None:
					self.sheet_obj.Cells(self.x1 + ix, self.y1 + iy).Value = one_value

	def write_formula(self, input_value):
		self.range_obj.Formula = input_value

	def write_formula_for_range(self, sheet_name, xyxy, input_value="=Now()"):
		"""
		영역에 입력으로 들어온 수식을 넣는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_formula_for_range(sheet_name="", xyxy="", input_value="=Now()")
			<object_name>.write_formula_for_range(("", "", "=Now()")
			<object_name>.write_formula_for_range((sheet_name="sht1", xyxy=[1,1,7,10], input_value="=Now())
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))
		range_obj.Formula = input_value

	def write_input_value_for_range_by_xy_step(self, sheet_name, xyxy, input_value, xy_step):
		"""
		선택한 영역의 시작점부터 x,y 번째 셀마다 값을 넣기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (any) 입력값
		:param xy_step: (list) [1, 1]의 형태로 나타내는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_input_value_for_range_by_xy_step(sheet_name="", xyxy="", input_value="입력값", xy_step=[1, 1])
			<object_name>.write_input_value_for_range_by_xy_step("", "", "입력값", [1, 1])
			<object_name>.write_input_value_for_range_by_xy_step(sheet_name="sht1", xyxy="", input_value="입력값", xy_step=[12, 13])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			if divmod(x, xy_step[0])[1] == 0:
				for y in range(y1, y2 + 1):
					if divmod(x, xy_step[1])[1] == 0:
						one_value = sheet_obj.Cells(x, y).Value2
						if one_value == None:
							one_value = ""
						sheet_obj.Cells(x, y).Value = one_value + str(input_value)

	def write_l1d_for_cell_as_group(self, sheet_name, xyxy, input_l1d):
		"""
		1차원자료를 시작셀을 기준으로 아래로 값을 넣는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param input_l1d: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_l1d_for_cell_as_group(sheet_name="", xyxy="", input_l1d=[1, "abc", "가나다"])
			<object_name>.write_l1d_for_cell_as_group("", [1,1,3,20], [1, "abc", "가나다"])
			<object_name>.write_l1d_for_cell_as_group("sht1", [1,1,1,20], [1, "abc", "가나다"])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		sheet_obj.Cells(x1, y1).Value = input_l1d

	def write_l1d_for_range_from_cell_as_yline_by_step(self, sheet_name, input_l1d, step_no, start_xy):
		"""
		1차원자료를 n개씩 세로로 써주는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_l1d: (list) 1차원의 list형 자료
		:param step_no: (int) 정수, n번째마다 반복되는것
		:param start_xy: (list or str) 셀영역으로 [1,2], ''(현재 선택 영역)로 사용가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_l1d_from_cell_as_yline_by_step(sheet_name="", step_no=5, input_l1d=[1, "abc", "가나다"], start_xy=[1, 1])
			<object_name>.write_l1d_from_cell_as_yline_by_step("", [1, "abc", "가나다"], 5, [1, 1])
			<object_name>.write_l1d_from_cell_as_yline_by_step(sheet_name="sht1", input_l1d=[1, "abc", "가나다"], step_no=5, start_xy=[1, 1])
		"""
		input_l1d = self.check_input_data(input_l1d)
		sheet_obj = self.check_sheet_name("")
		mok, namuji = divmod(len(input_l1d), step_no)
		if namuji > 0:
			mok = mok + 1
		y = 0
		count = 0
		for _ in range(mok):
			for ix in range(step_no):
				sheet_obj.Cells(ix + start_xy[0], y + start_xy[1]).Value = input_l1d[count]
				if len(input_l1d) == count + 1:
					return
				count = count + 1
			y = y + 1

	def write_l1d_from_cell(self, sheet_name, xy, input_l1d):
		"""
		1차원리스트의 값을 특정셀에서부터 다 써주는 것이다. 영역을 나타내는 xy변수의 기본값을 ""일때는 현재 선택된 영역을 뜻하는 것입니다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param input_l1d: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_l1d_from_cell(sheet_name="", xyxy="", input_l1d=[1, "abc", "가나다"])
			<object_name>.write_l1d_from_cell("", [1,1,3,20], [1, "abc", "가나다"])
			<object_name>.write_l1d_from_cell("sht1", [1,1,1,20], [1, "abc", "가나다"])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xy)

		sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x1, y1 + len(input_l1d) - 1)).Value = input_l1d

	def write_l1d_from_cell_as_yline(self, sheet_name, xyxy, input_l1d):
		"""
		1차원자료를 세로줄로 써내려가는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_l1d: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_l1d_from_cell_as_yline(sheet_name="", xyxy="", input_l1d=[1, "abc", "가나다"])
			<object_name>.write_l1d_from_cell_as_yline("", [1,1,3,20], [1, "abc", "가나다"])
			<object_name>.write_l1d_from_cell_as_yline("sht1", [1,1,1,20], [1, "abc", "가나다"])
		"""
		#속도를 높이기위해 변경함
		input_l1d = self.check_input_data(input_l1d)
		l2d = []
		for x, value in enumerate(input_l1d):
			l2d.append([value])
		self.write_as_value_priority(sheet_name, xyxy, l2d)

	def write_l1d_from_cell_as_yline_by_step(self, input_l1d, step_no, start_xy):
		"""
		공동변수를 이용해서 하나의 공통 변수를 이용하여 실행
		1차원의 자료를 n번째마다 입력갯수만큼 써주는 것이다
		:param input_l1d:
		:param step_no:
		:param start_xy:
		:return:
		"""
		input_l1d = self.check_input_data(input_l1d)
		mok, namuji = divmod(len(input_l1d), step_no)
		if namuji > 0:
			mok = mok + 1
		y = 0
		count = 0
		for _ in range(mok):
			for ix in range(step_no):
				self.sheet_obj.Cells(ix + start_xy[0], y + start_xy[1]).Value = input_l1d[count]
				if len(input_l1d) == count + 1:
					return
				count = count + 1
			y = y + 1

	def write_l1d_from_cell_by_step(self, sheet_name, xyxy, input_l1d, step_no):
		"""
		1차원자료를 n개로 분리해서 2차원자료처럼 만든후 값을 쓰는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_l1d: (list) 1차원의 list형 자료
		:param step_no: (int) 정수, n번째마다 반복되는것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_l1d_from_cell_by_step(sheet_name="", xyxy="", input_l1d=[1, "abc", "가나다"], step_no=5)
			<object_name>.write_l1d_from_cell_by_step("", "", [1, "abc", "가나다"], 3)
			<object_name>.write_l1d_from_cell_by_step(sheet_name="sht1", xyxy=[1,1,7,7,], input_l1d=[1, "abc", "가나다"], step_no=5)
		"""
		input_l1d = self.check_input_data(input_l1d)
		self.util.change_l1d_to_l2d_group_by_step(input_l1d, step_no)
		self.write_l2d_from_cell(sheet_name, xyxy, input_l1d)

	def write_l1d_to_ydirection(self, input_l1d):
		for index, one_value in enumerate(input_l1d):
			self.sheet_obj.Cells(self.x1, index + self.y1).Value = one_value

	def write_l2d_for_range(self, sheet_name, xyxy, input_l2d):
		"""
		2차원 리스트의 값을 영역에 쓰는것. 갯수가 크면, 그게 더 우선 된다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_l2d: (list) 2차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_l2d_for_range(sheet_name, xyxy, input_l2d)
			<object_name>.write_l2d_for_range("", [1,1,3,20], [[1,2,3],[4,5,6],[7,8,9])
			<object_name>.write_l2d_for_range("sht1", [1,1,1,20], [[1,2,3],[4,5,6],[7,8,9])
		"""
		self.write_auto(sheet_name, xyxy, input_l2d, "value")

	def write_l2d_for_range_from_start_cell_by_mixed_types(self, sheet_name, xyxy, input_l2d):
		"""
		여러가지 자료가 쉬여있는 자료를 쓰는것
		아래의 자료를 쓰기위한것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_l2d: (list) 2차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_l2d_from_start_cell_by_mixed_types(sheet_name, xyxy, input_l2d)
			<object_name>.write_l2d_from_start_cell_by_mixed_types("", [1,1,3,20], [[1,2,3],[4,5,6],[7,8,9])
			<object_name>.write_l2d_from_start_cell_by_mixed_types("sht1", [1,1,1,20], [[1,2,3],[4,5,6],[7,8,9])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		input_l2d = self.check_input_data(input_l2d)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		for x, l1d in enumerate(input_l2d):
			shift_y = 0
			for y, one_data in enumerate(l1d):
				if isinstance(one_data, str) or isinstance(one_data, int):
					# 문자나 숫자일때
					sheet_obj.Cells(x1 + x, y1 + shift_y).Value = one_data
					shift_y = shift_y + 1
				elif isinstance(one_data, list) or isinstance(one_data, int):
					# 리스트나 튜플일때
					for num, value in enumerate(one_data):
						sheet_obj.Cells(x1 + x, y1 + shift_y).Value = value
						shift_y = shift_y + 1
				elif isinstance(one_data, tuple):
					# 사전형식일때
					changed_list = list(one_data.items())
					for num, value in enumerate(changed_list):
						sheet_obj.Cells(x1 + x, y1 + shift_y).Value = value[0]
						shift_y = shift_y + 1
						sheet_obj.cel1s(x1 + x, y1 + shift_y).Value = value[1]
						shift_y = shift_y + 1

	def write_auto(self, sheet_name="", xyxy="", input_value=[], range_or_value_priority="value"):
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		changed_l2d = self.to_list_and_changing_date_type(input_value)
		len_x = len(changed_l2d)
		len_y = len(changed_l2d[0])

		if range_or_value_priority == "value":
			sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x1 + len_x - 1, y1 + len_y - 1)).Value = changed_l2d
		else:
			new_x = x2
			new_y = y2
			if x2 - x1 < len_x:
				new_x = x1 + len_x - 1
			if y2 - y1 < len_y:
				new_y = y1 + len_y - 1
			sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2)).Value = changed_l2d[:new_x][:new_y]

	def write_l2d_for_range_with_yline_no_at_one_line(self, sheet_name, input_xno, input_yno, input_l1d):
		"""
		같은 줄에 다른 값을 쓸때 사용. l2d= [[4, "박상진"], [5, title.strip()], [8, pr_no]]

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_yno: (int) 정수, 엑셀의 세로열(column) 번호를 나타내는것 가로의 숫자
		:param input_l1d: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_l2d_with_yline_no_at_one_line(sheet_name="", input_yno=5, input_l1d=[1, "abc", "가나다"])
			<object_name>.write_l2d_with_yline_no_at_one_line("", 5, [1, "abc", "가나다"])
			<object_name>.write_l2d_with_yline_no_at_one_line(sheet_name="sht1", input_yno=5, input_l1d=[1, "abc", "가나다"])
		"""
		sheet_obj = self.check_sheet_name("")

		for x_no, value in input_l1d:
			sheet_obj.Cells(input_xno+x_no, input_yno).Value = value

	def write_l2d_from_cell(self, sheet_name, xyxy, input_l2d):
		"""
		입력된 셀을 기준으로 2차원 리스트형태의 값을 쓰기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_l2d: (list) 2차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_l2d_from_cell(sheet_name, xyxy, input_l2d)
			<object_name>.write_l2d_from_cell("", [1,1,3,20], [[1,2,3],[4,5,6],[7,8,9])
			<object_name>.write_l2d_from_cell("sht1", [1,1,1,20], [[1,2,3],[4,5,6],[7,8,9])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		changed_l2d = self.to_list_and_changing_date_type(input_l2d)
		len_x = len(changed_l2d)
		len_y = len(changed_l2d[0])
		sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x1 + len_x - 1, y1 + len_y - 1)).Value = changed_l2d

	def write_l2d_with_yline_no_at_one_line(self, input_xno, input_yno, input_l1d):
		for x_no, value in input_l1d:
			self.sheet_obj.Cells(input_xno + x_no, input_yno).Value = value

	def write_list_for_range(self, sheet_name, xyxy, input_list):
		"""
		1차원의자료도 2차원으로 바꿔서, 값을 입력할 수 있다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_list_for_range(sheet_name="", xyxy="", input_list=[1, "abc", "가나다"])
			<object_name>.write_list_for_range("", [1,1,3,20], [1, "abc", "가나다"])
			<object_name>.write_list_for_range("sht1", [1,1,1,20], [1, "abc", "가나다"])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		changed_l2d = self.to_list_and_changing_date_type(input_list)
		len_x = len(changed_l2d)
		len_y = len(changed_l2d[0])
		sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x1 + len_x - 1, y1 + len_y - 1)).Value = changed_l2d

	def to_list_and_changing_date_type(self, data, none_is_none=False):
		"""
		기본으로 none은 빈문자열로 바꿔주며
		만약 듀플이있는 자료는 리스트로 변경을 해 주면서,
		날짜형식의 값을 변환해 주는것이다

		:param data:
		:return:
		"""
		if isinstance(data, (str, int, float, bool, dict, set)):
			return data
		if data is None:
			if none_is_none:
				return None
			else:
				return ""
		if isinstance(data, (tuple, list)):
			return [self.to_list_and_changing_date_type(item) for item in data]
		if isinstance(data, (pywintypes.TimeType, datetime)):
			try:
				has_time = (hasattr(data, 'hour') and (data.hour != 0 or data.minute != 0 or data.second != 0))
				if has_time:
					return data.strftime('%Y-%m-%d %H:%M:%S')
				return data.strftime('%Y-%m-%d')
			except (AttributeError, ValueError, OSError):
				return str(data)
		return str(data)

	def write_many_cell_at_same_xline(self, sheet_name, input_xno, yno_n_value_l2d):
		"""
		코드가 보기 편하게 나타내기 위해서 같은 줄의 여러값을 넣을때 이것을 사용하면 좋을듯 하다

		업무에서, 찾거나 변경된 자료를 일일이 넣는것은 코드가 너무 많아 보여서 좀 줄여보기위해서 만든다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_xno: (int) 정수, x를 나타내는 가로줄의 번호, row의 숫자번호
		:param yno_n_value_l2d: (list)
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_many_cell_at_same_xline(sheet_name="", input_xno=7, yno_n_value_l2d=[1, [[1, 2], [4, 5]]])
			<object_name>.write_many_cell_at_same_xline("", 5, yno_n_value_l2d=[1, [[1, 2], [4, 5]]])
			<object_name>.write_many_cell_at_same_xline(sheet_name="sht1", input_xno=3, yno_n_value_l2d=[2, [[1, 2], [4, 5]]])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		yno_n_value_l2d = self.check_input_data(yno_n_value_l2d)
		for yno, value in yno_n_value_l2d:
			sheet_obj.Cells(input_xno, yno).Value = value

	def write_memo(self, input_value):
		"""
		하나의 셀에 메모를 작성하는 것
		:param input_value:
		:return:
		"""
		if self.range_obj.Comment:
			input_value = self.range_obj.Comment.Text()
			self.range_obj.Comment.Text(str(input_value) + str(input_value))
		else:
			self.range_obj.AddComment(input_value)

	def write_memo_for_cell_with_replace(self, sheet_name, xyxy, input_value):
		"""
		셀에 메모를 넣는것. 기존에 메모가 있으면 내용이 변경된다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param text: (str) 입력으로 들어오는 텍스트, 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_memo_for_cell_with_replace(sheet_name="", xyxy="", input_value="메모 입력")
			<object_name>.write_memo_for_cell_with_replace("", [1,1],"메모 입력")
			<object_name>.write_memo_for_cell_with_replace("sht1", [1,20],"메모 입력")
		"""
		self.write_memo_for_cell(sheet_name, xyxy, input_value)

	def write_nansu(self, start_no, end_no):
		basic_data = list(range(start_no, end_no + 1))
		random.shuffle(basic_data)
		temp_no = 0
		for x in range(self.x1, self.x2 + 1):
			for y in range(self.y1, self.y2 + 1):
				self.sheet_obj.Cells(x, y).Value = basic_data[temp_no]
				if temp_no >= end_no - start_no:
					random.shuffle(basic_data)
					temp_no = 0
				else:
					temp_no = temp_no + 1

	def write_nansu_for_range(self, sheet_name, xyxy, start_no, end_no):
		"""
		입력한 숫자범위에서 난수를 만들어서 영역에 써주는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_list: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_nansu_for_range(sheet_name="", xyxy="", input_list=[1, 100])
			<object_name>.write_nansu_for_range("sht1", "", [1,20])
			<object_name>.write_nansu_for_range("", "", [20, 50])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		basic_data = list(range(start_no, end_no + 1))
		random.shuffle(basic_data)
		temp_no = 0
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				sheet_obj.Cells(x, y).Value = basic_data[temp_no]
				if temp_no >= end_no - start_no:
					random.shuffle(basic_data)
					temp_no = 0
				else:
					temp_no = temp_no + 1

	def write_searched_value_at_different_cell(self, xyxy="", value_line_no=2, changed_value_line_no=3, result_line_no=4, input_xre="[시작:처음][영어:1~4][한글:3~10]"):
		"""
		선택한 영역의 모든 셀의 값에대하여, 정규표현식으로 찾은 값을 나열하는 것. 1개의 라인만 적용을 해야 한다

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		value-line_no : 정규표현식을 적용할 y 라인
		changed_value_line-no : (int) value_line_no의 값을 바꾼후의 값, False값이면 적용되지 않는다
		result_line_no : (int) 찾은 값을 쓰는 첫번째 라인
		input_xre : (str) xre형식의 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_searched_value_at_different_cell(xyxy="", value_line_no=2, changed_value_line_no=3, result_line_no=4, input_xre="[시작:처음][영어:1~4][한글:3~10]")
			<object_name>.write_searched_value_at_different_cell("", 3, 3, 4, "[시작:처음][영어:1~4][한글:3~10]")
			<object_name>.write_searched_value_at_different_cell(xyxy="sht1", value_line_no=3, changed_value_line_no=7, result_line_no=4, input_xre="[시작:처음][영어:1~4][한글:3~10]")
		"""
		sheet_obj = self.check_sheet_name("")
		all_data = self.read_value_for_range("", xyxy)  # 1
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		for index, l1d in enumerate(all_data):
			current_x = x1 + index
			if l1d:
				value = str(l1d[value_line_no]).lower().strip()
				found = self.rex.search_all_by_xsql(input_xre, value)  # 정규표현식에 맞는 값을 확인
				# [[결과값, 시작순서, 끝순서, [그룹1, 그룹2...], match결과].....]
				if found:  # 만약 발견하면
					gijon = self.read_value_for_cell("", [current_x, result_line_no])
					changed_gijon = gijon + "," + l1d[0] + ":" + str(l1d[1]) + ":" + str(l1d[2])
					if not changed_value_line_no:
						sheet_obj.Cells(current_x, result_line_no).Value = current_x, result_line_no

	def write_serial_date_by_step(self, start_day, day_step, multi_line):
		timex = xy_time.xy_time()
		base_dt_obj = timex.change_anytime_to_dt_obj(start_day)

		if not multi_line: self.y2 = self.y1
		repeat_no = 0
		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			dt_obj_1 = timex.shift_day_for_dt_obj(base_dt_obj, day_step * repeat_no)
			self.sheet_obj.Cells(x, y).Value = timex.change_dt_obj_to_yyyy_mm_dd(dt_obj_1)
			repeat_no = repeat_no + 1

	def write_serial_date_for_range_by_step(self, sheet_name, xyxy, start_day="2025-03-01", day_step=1, multi_line=False):
		"""
		어떤 날자를 기준으로 연속해서 날짜를 넣는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param start_day: date) 2025-05-15형식의 날짜형식의 자료
		:param day_step: (int) 날짜의 차이를 나타내는 숫자
		:param multi_line: (bool) 여러줄로 나타내는 것을 설정하는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_serial_date_by_step(sheet_name="", xyxy="", start_day="2025-03-01", day_step=1, multi_line=False)
			<object_name>.write_serial_date_by_step("sht1", [1,1, 3, 20], start_day="2025-03-01", day_step=1, multi_line=False)
			<object_name>.write_serial_date_by_step("", "", "2025-03-01", 1)
		"""
		timex = xy_time.xy_time()
		sheet_obj = self.check_sheet_name(sheet_name)
		base_dt_obj = timex.change_anytime_to_dt_obj(start_day)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		if not multi_line: y2 = y1
		repeat_no = 0
		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				dt_obj_1 = timex.shift_day_for_dt_obj(base_dt_obj, day_step * repeat_no)
				sheet_obj.Cells(x, y).Value = timex.change_dt_obj_to_yyyy_mm_dd(dt_obj_1)
				repeat_no = repeat_no + 1

	def write_serial_no(self, start_no, step_no, ydirection_tf=True):
		new_no = start_no
		if ydirection_tf:
			for no in range(0, self.x2 - self.x1 + 1):
				self.sheet_obj.Cells(self.x1 + no, self.y1).Value = new_no
				new_no = new_no + step_no
		else:
			for no in range(0, self.x2 - self.x1 + 1):
				self.sheet_obj.Cells(self.x1, self.y1 + no).Value = new_no
				new_no = new_no + step_no

	def write_serial_no_for_range_by_step(self, sheet_name, xyxy, start_no, step_no):
		"""
		선택한 영역에 시작번호, 간격으로 이루어진 연속된 숫자를 쓰는것

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param start_no: (int) 정수
		:param step_no: (int) 정수, n번째마다 반복되는것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_serial_no_by_step(xyxy="", start_no=1, step_no=1)
			<object_name>.write_serial_no_by_step("", 2, 3])
			<object_name>.write_serial_no_by_step_no_to_yline("", 4, 10])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)
		range_obj = sheet_obj.Range(sheet_obj.Cells(x1, y1), sheet_obj.Cells(x2, y2))

		count = 0
		update_no = start_no
		for x in range(0, x2 - x1 + 1):
			for y in range(0, y2 - y1 + 1):
				count = count + 1
				if divmod(count, step_no)[1] == 0:
					sheet_obj.Cells(x, y).Value = update_no
					update_no = update_no + step_no

	def write_serial_no_for_range_by_step_to_xline(self, xyxy, start_no, step_no):
		"""
		선택한 영역에 시작번호, 간격으로 이루어진 연속된 숫자를 쓰는것 (예 : 0,2,4,6,8....)

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param start_no: (int) 정수
		:param step_no: (int) 정수, n번째마다 반복되는것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_serial_no_for_range_by_step_to_xline(xyxy="", start_no=1, step_no=1)
			<object_name>.write_serial_no_for_range_by_step_to_xline("", 2, 3])
			<object_name>.write_serial_no_for_range_by_step_to_xline("", 4, 10])
		"""
		sheet_obj = self.check_sheet_name("")
		new_no = start_no
		for no in range(0, xyxy[2] - xyxy[0] + 1):
			sheet_obj.Cells(xyxy[0], xyxy[1] + no).Value = new_no
			new_no = new_no + step_no

	def write_serial_no_for_range_by_step_to_yline(self,sheet_name, xyxy, start_no, step_no):
		"""
		선택한 영역에 시작번호, 간격으로 이루어진 연속된 숫자를 쓰는것

		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param start_no: (int) 정수
		:param step_no: (int) 정수, n번째마다 반복되는것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_serial_no_by_step_to_yline(xyxy="", start_no=1, step_no=1)
			<object_name>.write_serial_no_by_step_to_yline("", 2, 3])
			<object_name>.write_serial_no_by_step_no_to_yline("", 4, 10])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		new_no = start_no
		for no in range(0, xyxy[2] - xyxy[0] + 1):
			sheet_obj.Cells(xyxy[0] + no, xyxy[1]).Value = new_no
			new_no = new_no + step_no

	def write_serial_no_for_range_with_start_no(self, sheet_name, xyxy, start_no, step_no):
		"""
		숫자를 주면 시작점부터 아래로 숫자를 써내려가는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param start_no: (int) 정수
		:param step_no: (int) 정수, n번째마다 반복되는것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_serial_no_with_start_no(sheet_name="",xyxy="", start_no=1, step_no=1)
			<object_name>.write_serial_no_with_start_no("", "", 2, 3])
			<object_name>.write_serial_no_with_start_no("sht1", "", 4, 10])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		new_no = start_no
		for no in range(0, x2 - x1 + 1):
			sheet_obj.Cells(x1 + no, y1).Value = new_no
			new_no = new_no + step_no

	def write_sum_result_from_xy_for_l2d(self, input_l2d, xy):
		"""
		선택한 영역의 세로 자료들을 다 더해서 제일위의 셀에 다시 넣는것

		:param input_l2d: (list) 2차원의 list형 자료
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_sum_result_from_xy_for_l2d(input_l2d=[[1, 2], [4, 5]], xy="")
			<object_name>.write_sum_result_from_xy_for_l2d([[1, 2], [4, 5]], [1,1])
			<object_name>.write_sum_result_from_xy_for_l2d([[1, 2], [4, 5]], [7,20])
		"""
		sheet_obj = self.check_sheet_name("")
		input_l2d = self.check_input_data(input_l2d)

		x_len = len(input_l2d)
		y_len = len(input_l2d[0])
		for y in range(y_len):
			temp = ""
			for x in range(x_len):
				sheet_obj.Cells(x + xy[0], y + xy[1]).Value = ""
				if input_l2d[x][y]:
					temp = temp + " " + input_l2d[x][y]
			sheet_obj.Cells(xy[0], y + xy[1]).Value = str(temp).strip()

	def write_test_data(self, data_type, input_value):
		if data_type == "l1d":
			data = self.varx["data"][input_value]
			self.new_sheet()
			self.write_l1d_for_yline("", [1,1], data)
		elif data_type == "l2d":
			data = self.varx["data"][input_value]
			self.new_sheet()
			self.write_value_for_range("", [1,1], data)
		elif data_type == "t2d":
			data = self.varx["data"][input_value]
			changed_data = data.splitlines()
			self.new_sheet()
			self.write_l1d_for_yline("", [1,1], changed_data)
		elif data_type == "table2d":
			data = self.varx["data"][input_value]
			self.new_sheet()
			self.write_value_for_range("", [1,1], data)
		elif data_type == "d1d":
			data = self.varx["data"][input_value]
			self.new_sheet()
			for index, key in enumerate(data.keys()):
				self.write_cell("", [1+index, 1], key)
				self.write_cell("", [1+index, 2], str(data[key]))
		elif data_type == "d2d":
			data = self.varx["data"][input_value]
			self.new_sheet()
			for index, key in enumerate(data.keys()):
				self.write_cell("", [1+index, 1], key)
				self.write_cell("", [1+index, 2], str(data[key]))

	def write_title_from_first_line(self):
		all_data = []
		for y in range(self.y1, self.y2 + 1):
			xylist_data = []
			for x in range(self.x1, self.x2 + 1):
				# 병합이 있는 자료를 위해서 필요한 것이다
				aa = self.is_merged_cell([x, y])
				if aa:
					value = self.read([aa[2][0], aa[2][1]])
				else:
					value = self.read([x, y])

				# 양쪽 공백을 없앤다
				value = str(value).strip()
				xylist_data.append(value)

			# 2줄 이상의 제목라인이 있을때, 위 아래의것을 합치기 위해서 필요
			final_title = ""
			for one in xylist_data:
				if one:
					final_title = final_title + one + "_"
			# 아무런 제목도 없을경우는 가로의 숫자를 이용해서 만든 제목을 넣는다
			if final_title == "":
				final_title = "title_" + str(y) + "_"

			# 소문자로 만든다
			final_title = str(final_title[:-1]).lower()

			for bb in [[" ", "_"], ["&", ""], ["&", ""], ["(", ""], [")", ""], ["/", ""], ["-", ""], [".", ""],
					   ["%", ""]]:
				final_title = final_title.replace(bb[0], bb[1])

	def write_title_from_first_line_for_range(self, sheet_name, xyxy):
		"""
		영역을 주면, 제일 첫번째 라인의 값들을 적절한 형태로 제목으로 만들어 주는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_title_from_first_line_for_range(sheet_name="", xyxy="")
			<object_name>.set_title_from_first_line_for_range("sht1", [1,1,3,20])
			<object_name>.set_title_from_first_line_for_range("", "")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		all_data = []
		for y in range(xyxy[1], xyxy[3] + 1):
			xylist_data = []
			for x in range(xyxy[0], xyxy[2] + 1):
				# 병합이 있는 자료를 위해서 필요한 것이다
				aa = self.check_merge_status_for_cell(sheet_name, [x, y])
				if aa:
					value = self.read_value_for_cell(sheet_name, [aa[2][0], aa[2][1]])
				else:
					value = self.read_value_for_cell(sheet_name, [x, y])

				# 양쪽 공백을 없앤다
				value = str(value).strip()
				xylist_data.append(value)

			# 2줄 이상의 제목라인이 있을때, 위 아래의것을 합치기 위해서 필요
			final_title = ""
			for one in xylist_data:
				if one:
					final_title = final_title + one + "_"
			# 아무런 제목도 없을경우는 가로의 숫자를 이용해서 만든 제목을 넣는다
			if final_title == "":
				final_title = "title_" + str(y) + "_"

			# 소문자로 만든다
			final_title = str(final_title[:-1]).lower()

			for bb in [[" ", "_"], ["&", ""], ["&", ""], ["(", ""], [")", ""], ["/", ""], ["-", ""], [".", ""],
					   ["%", ""]]:
				final_title = final_title.replace(bb[0], bb[1])

	def write_value_at_end_of_column(self, sheet_name, xy, input_l1d):
		"""
		** 보관용
		a3을 예로들어서, a3을 기준으로, 입력한 값이있는제일 마지막 가로줄번호를 갖고온후,
		그 다음줄에 값을 넣는것
		어떤 선택된 자료의 맨 마지막에 값을 넣기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param input_l1d: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_value_at_end_of_column(sheet_name="", xy=[1,3], input_l1d=[1, "abc", "가나다"])
			<object_name>.write_value_at_end_of_column("", [1,3], [1, "abc", "가나다"])
			<object_name>.write_value_at_end_of_column(sheet_name="sht1", xy=[5,7], input_l1d=[17,"abc","가나다"])
		"""
		self.move_activecell_for_range_to_bottom(sheet_name, xy)
		xy = self.read_address_for_activecell()
		self.write_value_for_range(sheet_name, [xy[0] + 1, xy[1]], input_l1d)

	def write_value_by_xy_step(self, input_value, xy_step):
		for x in range(self.x1, self.x2 + 1):
			if divmod(x, xy_step[0])[1] == 0:
				for y in range(self.y1, self.y2 + 1):
					if divmod(y, xy_step[1])[1] == 0:
						self.sheet_obj.Cells(x, y).Value = str(input_value)

	def write_value_by_xy_step_for_range(self, sheet_name, xyxy, input_value, xy_step):
		"""
		영역에 입력값을 쓰는 것이며, 선택한 영역의 시작점부터 x,y 번째 셀마다 입력값을 쓰기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (any) 입력값
		:param xy_step: (list) [1, 1]의 형태로 나타내는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_one_value_by_xy_step(sheet_name="", xyxy="", input_value="입력값", xy_step=[1, 1])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			if divmod(x, xy_step[0])[1] == 0:
				for y in range(y1, y2 + 1):
					if divmod(y, xy_step[1])[1] == 0:
						sheet_obj.Cells(x, y).Value = input_value

	def write_value_for_activecell(self, input_value):
		"""
		활성화된 셀에 입력된 값을 쓰기

		:param input_value: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_value_for_activecell("입력값")
			<object_name>.write_value_for_activecell(123)
		"""
		sheet_obj = self.check_sheet_name("")
		x1, y1, x2, y2 = self.change_any_address_to_xyxy("")
		sheet_obj.Cells(x1, y1).Value = input_value

	def write_value_for_cell(self, sheet_name, xyxy, input_value):
		"""
		셀에 값는 넣기, write_cell을 사용하는것이 더 이해하기 쉽다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_value_for_cell(sheet_name="", xyxy="", input_value="입력값")
			<object_name>.write_value_for_cell("", "", "입력값")
			<object_name>.write_value_for_cell("sht1", [1,1,7,10], "입력값")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		input_value = self.check_input_data(input_value)
		sheet_obj.Cells(x1, y1).Value = input_value

	def write_value_for_cell_as_linked(self, sheet_name, xy, web_site_address="www.google.co.kr", tooltip=""):
		"""
		값을 쓰면서, 링크를 거는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param web_site_address: (str) 웹사이트 주소
		:param tooltip: (str) 툴팁에 나타날 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_value_for_cell_as_linked(sheet_name="", xy="", web_site_address="www.google.co.kr", tooltip="툴팁내용")
			<object_name>.write_value_for_cell_as_linked("", "", "www.google.co.kr", "툴팁내용")
			<object_name>.write_value_for_cell_as_linked(sheet_name="sht1", xy=[1,1,1,20], web_site_address="www.google.co.kr", tooltip="툴팁내용")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xy)
		sheet_obj.Hyperlinks.Add(Anchor=sheet_obj.Cells(x1, y1), Address=web_site_address, ScreenTip=tooltip)

	def write_value_for_range(self, sheet_name, xyxy, input_value):
		"""
		영역에 값 넣기, 영역과 값의 갯수가 틀리면, 값이 우선임
		하나하나 입력이 되는 모습을 보여주면서 실행된다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_value_for_range(sheet_name="", xyxy="", input_value="입력값")
			<object_name>.write_value_for_range("", [1,1,3,20], "입력값")
			<object_name>.write_value_for_range("sht1", [1,1,1,20], "입력값")
		"""
		input_value = self.check_input_data(input_value)
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		checked_l2d = self.util.change_any_data_to_l2d(input_value)

		for index, l1d in enumerate(checked_l2d):
			r1c1 = self.xyxy2_to_r1c1([x1 + index, y1, x1 + index, y1 + len(l1d) - 1])
			sheet_obj.Range(r1c1).Value = l1d

	def write_value_for_range_as_linked(self, sheet_name, xy, web_site_address="www.google.co.kr", tooltip=""):
		"""
		값을 쓰면서, 링크를 거는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xy: (list or str) [1,2], 가로세로셀영역 , ""은 현재 셀영역을 뜻함
		:param web_site_address: (str) 웹사이트 주소
		:param tooltip: (str) 툴팁에 나타날 문자열
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_cell_as_linked(sheet_name="", xy="", web_site_address="www.google.co.kr", tooltip="툴팁내용")
			<object_name>.write_cell_as_linked("", "", "www.google.co.kr", "툴팁내용")
			<object_name>.write_cell_as_linked(sheet_name="sht1", xy=[1,1,1,20], web_site_address="www.google.co.kr", tooltip="툴팁내용")
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.change_any_address_to_xyxy(xy)

		sheet_obj.Hyperlinks.Add(Anchor=sheet_obj.Cells(x1, y1), Address=web_site_address, ScreenTip=tooltip)

	def write_value_for_range_by_range_priority(self, sheet_name, xyxy, input_l2d):
		"""
		영역에 입력값을 쓰는 것인데, 만약 영역안의 셀의 갯수와 입력 자료의 갯수가 틀릴때, 영역을 기준으로 값을 쓰는 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_l2d: (list) 2차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_value_for_range_by_range_priority(sheet_name, xyxy, input_l2d)
			<object_name>.write_value_for_range_by_range_priority("", [1,1,3,20], [[1, 2], [4, 5]])
			<object_name>.write_value_for_range_by_range_priority("sht1", [1,1,1,20], input_l2d=[[1, 2], [4, 5]])
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		input_l2d = self.check_input_data(input_l2d)

		for index, l1d in enumerate(input_l2d):
			if index >= x2 - x1 + 1:
				break
			else:
				if len(l1d) > y2 - y1 + 1:
					r1c1 = self.xyxy2_to_r1c1([x1 + index, y1, x1 + index, y2])
					sheet_obj.Range(r1c1).Value = l1d[:y2 - y1 + 1]
				else:
					r1c1 = self.xyxy2_to_r1c1([x1 + index, y1, x1 + index, y1 + len(l1d) - 1])
					sheet_obj.Range(r1c1).Value = l1d

	def write_value_for_range_by_reverse(self, sheet_name, xyxy):
		"""
		영역에 입력값을 쓰는 것이며, 현재 입력한 영역의 값을 읽어와서, 입력자료를 좌우를 바꾸는 형태로(xy를 yx로 바꿔서) 입력하는 것이다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param l2d: (list) 2차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_value_for_range_by_reverse(sheet_name="", xyxy="")
			<object_name>.write_value_for_range_by_reverse("sht1", [1,1,3,20])
			<object_name>.write_value_for_range_by_reverse("", "")
		"""
		l2d = self.read_value_for_range(sheet_name, xyxy)
		changed_l2d = []
		for y in range(len(l2d[0])):
			temp = []
			for x in range(len(l2d)):
				temp.append(l2d[x][y])
			changed_l2d.append(temp)
		self.new_sheet()
		self.write_l2d_from_cell("", [1, 1], changed_l2d)

	def write_value_for_range_by_value_priority(self, sheet_name, xyxy, input_l2d):
		"""
		영역에 입력값을 쓰는 것이며, 선택한 영역의 갯수와 입력자료의 갯수가 틀릴때 , 입력자료의 갯수를 우선으로 쓰는것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_l2d: (any) 입력값
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_value_for_range_by_value_priority(sheet_name, xyxy, input_l2d)
			<object_name>.write_value_for_range_by_value_priority("", [1,1,3,20], [[1, 2], [4, 5]])
			<object_name>.write_value_for_range_by_value_priority("sht1", [1,1,1,20], input_l2d)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		input_l2d = self.check_input_data(input_l2d)
		r1c1 = self.xyxy2_to_r1c1([x1, y1, x1 + len(input_l2d) - 1, y1 + len(input_l2d[0]) - 1])
		sheet_obj.Range(r1c1).Value = input_l2d

	def write_value_for_range_by_xy_step(self, sheet_name, xyxy, input_value, xy_step):
		"""
		영역에 입력값을 쓰는 것이며, 선택한 영역의 시작점부터 x,y 번째 셀마다 입력값을 쓰기

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_value: (any) 입력값
		:param xy_step: (list) [1, 1]의 형태로 나타내는 것
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_value_for_range_by_xy_step(sheet_name="", xyxy="", input_value="입력값", xy_step=[1, 1])
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for x in range(x1, x2 + 1):
			if divmod(x, xy_step[0])[1] == 0:
				for y in range(y1, y2 + 1):
					if divmod(y, xy_step[1])[1] == 0:
						sheet_obj.Cells(x, y).Value = str(input_value)

	def write_value_for_range_except_none(self, sheet_name, xyxy, input_l2d):
		"""
		입력값안에 들어있는 None은 값을 쓰지 않고 건너띄는 형식으로 입력한다. 즉, 자료를 변경하고싶지 않을때는 None으로 그위치에 넣으면, 기존의 값이 보존 된다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_l2d: (list) 2차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_value_for_range_except_none(sheet_name="", xyxy="", input_l2d=[[1, 2, 3], [4, None, 6], [7, 8, 9]])
			<object_name>.write_value_for_range_except_none("", [1,1,3,20], [[1, None, 3], [4, 5, 6], [7, 8, 9]])
			<object_name>.write_value_for_range_except_none("sht1", [1,1,1,20], input_l2d=[[1, None, 3], [4, 5, 6], [7, 8, 9]])
		"""

		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)
		input_l2d = self.check_input_data(input_l2d)

		for ix, l1d in enumerate(input_l2d):
			for iy, one_value in enumerate(l1d):
				if one_value != None:
					sheet_obj.Cells(x1 + ix, y1 + iy).Value = one_value

	def write_value_for_range_to_ydirection_only(self, sheet_name, xyxy, input_l1d):
		"""
		영역의 첫번째 셀을 기준으로 1차원 리스트의 자료를 아래(가로)로 쓰는것, 만약 영역보다 갯수 많으면, 갯수가 우선된다

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param xyxy: (list or str) 영역을 나타내며, ''(현재 선택영역), A1:B3, [1,1,2,2]의 형태가 가능
		:param input_l1d: (list) 1차원의 list형 자료
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_value_for_range_to_ydirection_only(sheet_name="", xyxy="", input_l1d=[1,2,3,4,5])
			<object_name>.write_value_for_range_to_ydirection_only("", [1,1,3,20], [1,2,3,4,5])
			<object_name>.write_value_for_range_to_ydirection_only("sht1", [1,1,1,20], list_1d)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.change_any_address_to_xyxy(xyxy)

		for index, one_value in enumerate(input_l1d):
			sheet_obj.Cells(x1, index + y1).Value =one_value

	def write_value_in_statusbar(self, input_value):
		"""
		스테이터스바에 글씨를 쓰는 것, 변경하거나 알리고싶은 내용을 나타낼수 있다

		:param input_value: (str) 입력으로 들어오는 텍스트
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_value_in_statusbar("오늘은 금요일 입니다")
		"""
		input_value = self.check_input_data(input_value)
		self.xlapp.StatusBar = input_value

	def write_vba_module_for_workbook(self, vba_code, macro_name):
		"""
		텍스트로 만든 엑셀 매크로 코드를 현재 열려있는 엑셀화일에 vba모듈을 만드는 것이다

		:param vba_code: (str) 입력으로 들어오는 텍스트, vba코드
		:param macro_name: (str) 입력으로 들어오는 텍스트, 매크로이름
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_vba_module_for_workbook(vba_code1, macro_name1)
		"""
		new_vba_code = "Sub " + macro_name + "()" + vba_code + "End Sub"
		mod = self.xlbook.VBProject.VBComponents.Add(1)
		mod.CodeModule.AddFromString(new_vba_code)

	def write_with_link(self, xy, web_site_address, tooltip):
		self.set_range(xy)
		self.sheet_obj.Hyperlinks.Add(Anchor=self.sheet_obj.Cells(self.x1, self.y1), Address=web_site_address,
									  ScreenTip=tooltip)

	def write_with_new_sheet(self, input_value, start_xy):
		"""
		새로운 시트를 만들면서 값을 넣는것이며, 어떤 형태의 값이라도 알아서 써준다

		:param input_value: (any) 입력값
		:param start_xy: 자료가 써지는 시작점을 가르킵니다
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.write_with_new_sheet(input_value, start_xy=[3,4])
			<object_name>.write_with_new_sheet("입력값")
		"""
		self.new_sheet()
		if start_xy:
			x1, y1, x2, y2 = self.change_any_address_to_xyxy(start_xy)
			self.write_value_for_range("", [x1, y1], input_value)
		else:
			self.write_value_for_range("", [1,1], input_value)

	def xline_height_for_range(self, sheet_name, input_xno=7, height_float=13.5):
		"""
		높이를 설정하는 것

		:param sheet_name: (str) 시트이름, ""은 현재 활성화된 시트이름을 뜻함
		:param input_xno: (int) 정수, x를 나타내는 가로줄의 번호, row의 숫자번호
		:param height_float: (int) 높이를 나타내는 정수
		:return: None
		Examples
		--------
		.. code-block:: python
			<object_name>.set_height_for_xline(sheet_name="", input_xno=7, height_float=13.5)
			<object_name>.set_height_for_xline("", input_xno=3, height_float=13.5)
			<object_name>.set_height_for_xline(sheet_name="sht1", input_xno=9, height_float=23.5)
		"""
		sheet_obj = self.check_sheet_name(sheet_name)
		sheet_obj.Cells(input_xno, 1).EntireRow.RowHeight = height_float

	def write_today(self, style="yyyy-mm-dd"):
		dt_today = self.timex.get_dt_obj_for_today()
		formatted_day = self.timex.change_dt_to_user_style(dt_today, style)
		self.sheet_obj.Cells(self.x1, self.y1).Value = formatted_day

	def write_dt_obj(self, input_dt, style="yyyy-mm-dd"):
		formatted_day = self.timex.change_dt_to_user_style(input_dt, style)
		self.sheet_obj.Cells(self.x1, self.y1).Value = formatted_day

	def write_random(self, input_lid):
		l2d = self.util.change_any_data_to_l2d(input_lid)
		changed_l1d = self.util.change_l2d_to_l1d(l2d)
		random.shuffle(changed_l1d)
		count_data = len(changed_l1d)
		temp_no = 0

		for x, y in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
			if divmod(x+y, count_data)[0] == 0:
				random.shuffle(changed_l1d)
				temp_no = 0
			self.sheet_obj.Cells(x, y).Value = changed_l1d[temp_no]
			temp_no = temp_no + 1

	def check_list_or_srt_for_range(self, input_data):
		if isinstance(input_data, list):
			if len(input_data) == 1:
				start = input_data[0]
				end = input_data[0]
			else:
				start = input_data[0]
				end = input_data[1]
		else:
			start = input_data
			end = input_data
		return [start, end]

	def check_one_datafor_range(self, input_data):
		if isinstance(input_data, list):
			dest = input_data[0]
		else:
			dest = input_data
		return dest

	def move_yline(self, yyline1, yline2):
		"""
		선택한 세로줄(열)들을 특정 위치로 잘라내어 삽입(이동)합니다.

        :param yyline1: 잘라낼 열 번호. 단일 숫자(1), 문자("A"), 또는 범위([1, 5]) 가능
        :param yline2: 삽입될 목표 열 번호 (해당 열 앞에 삽입됨)
		"""
		[start, end] = self.check_list_or_srt_for_range(yyline1)
		dest = self.check_one_datafor_range(yline2)

		target_range = self.sheet_obj.Range(self.sheet_obj.Columns(start),self.sheet_obj.Columns(end))
		target_range.Cut()

		dest_range = self.sheet_obj.Columns(dest)
		dest_range.Insert(Shift=-4161)
		self.sheet_obj.Application.CutCopyMode = False

	def move_xline(self, xxline1, xline2):
		"""
		선택한 가로줄(행)들을 특정 위치로 잘라내어 삽입(이동)합니다.

        :param xxline1: 잘라낼 행 번호. 단일 숫자(1) 또는 범위([1, 5]) 가능
        :param xline2: 삽입될 목표 행 번호 (해당 행 위에 삽입됨)
		"""
		[start, end] = self.check_list_or_srt_for_range(xxline1)
		dest = self.check_one_datafor_range(xline2)

		target_range = self.sheet_obj.Range(self.sheet_obj.Rows(start),	self.sheet_obj.Rows(end))
		target_range.Cut()

		dest_range = self.sheet_obj.Rows(dest)
		dest_range.Insert(Shift=-4121)
		self.sheet_obj.Application.CutCopyMode = False

	def move_range(self, range_from, range_to, shift_direction='down'):
		"""
		특정 영역(Block)을 다른 위치로 이동시킵니다.

        :param range_from: 이동할 영역 주소 ([시작행, 시작열, 끝행, 끝열] 또는 "A1:C5")
        :param range_to: 붙여넣을 시작 셀 ([행, 열] 또는 "E10")
        :param overwrite: True이면 덮어쓰기, False이면 기존 셀을 밀어내며 삽입
		:return:
		"""
		# 엑셀 상수 설정
		xlShiftDown = -4121
		xlShiftToRight = -4161
		shift_val = xlShiftDown if shift_direction == 'down' else xlShiftToRight

		# 1. 소스 영역(from) 설정
		if isinstance(range_from, list):
			# [시작행, 시작열, 끝행, 끝열]
			s_row, s_col, e_row, e_col = range_from
			source_range = self.sheet_obj.Range(
				self.sheet_obj.Cells(s_row, s_col),
				self.sheet_obj.Cells(e_row, e_col)
			)
		else:
			# "A1:C5" 형태의 문자열
			source_range = self.sheet_obj.Range(range_from)

		# 2. 대상 위치(to) 설정
		if isinstance(range_to, list):
			# [행, 열]
			d_row, d_col = range_to
			dest_cell = self.sheet_obj.Cells(d_row, d_col)
		else:
			# "E10" 형태의 문자열
			dest_cell = self.sheet_obj.Range(range_to)

		# 3. 이동 실행 (Cut & Insert)
		source_range.Cut()
		dest_cell.Insert(Shift=shift_val)

		# 잘라내기 모드 해제
		self.sheet_obj.Application.CutCopyMode = False


	def overwrite_range(self, xyxy_from, xyxy_to, move=True):
		"""
		특정 영역을 다른 위치에 덮어씁니다.

		:param xyxy_from:[시작행, 시작열, 끝행, 끝열] 또는 "A1:C5"
		:param xyxy_to:[행, 열] 또는 "E10" (시작 지점만 지정)
		:param move:True이면 이동(기존 위치 삭제), False이면 복사
		:return:
		"""
		if isinstance(xyxy_from, list):
			source_range = self.sheet_obj.Range(
				self.sheet_obj.Cells(xyxy_from[0], xyxy_from[1]),
				self.sheet_obj.Cells(xyxy_from[2], xyxy_from[3])
			)
		else:
			source_range = self.sheet_obj.Range(xyxy_from)

		# 2. 대상 위치(to) 설정 (시작 셀 하나만 지정해도 됨)
		if isinstance(xyxy_to, list):
			dest_cell = self.sheet_obj.Cells(xyxy_to[0], xyxy_to[1])
		else:
			dest_cell = self.sheet_obj.Range(xyxy_to)

		# 3. 덮어쓰기 실행
		if move:
			# Destination을 지정하면 바로 덮어쓰기가 됩니다.
			source_range.Cut(Destination=dest_cell)
		else:
			source_range.Copy(Destination=dest_cell)

		# 선택 영역 점선 해제
		self.sheet_obj.Application.CutCopyMode = False

	def delete_xrange_value(self, input_no, step_on=False):
		"""
		설정된 영역(self.range_obj) 내에서 n번째 가로줄(행)의 값만 삭제합니다.

        :param input_no: 삭제할 상대적인 행 번호 (영역 내 첫 줄은 1)
        :param step_on: True일 경우 input_no의 배수 행들을 반복적으로 삭제
		:return:
		"""
		total_rows = self.range_obj.Rows.Count

		# 2. 삭제 로직
		if step_on:
			# 반복 삭제 (n, 2n, 3n...)
			# 범위를 벗어나지 않을 때까지 n의 배수 행을 삭제
			current_step = input_no
			while current_step <= total_rows:
				self.range_obj.Rows(current_step).ClearContents()
				current_step += input_no
		else:
			# n번째 한 줄만 삭제
			if input_no <= total_rows:
				self.range_obj.Rows(input_no).ClearContents()
		self.sheet_obj.Application.CutCopyMode = False

	def delete_yrange_value(self, input_no, step_on=False):
		"""
		설정된 영역(self.range_obj) 내에서 n번째 세로줄(열)의 값만 삭제합니다.

        :param input_no: 삭제할 상대적인 열 번호 (영역 내 첫 열은 1)
        :param step_on: True일 경우 input_no의 배수 열들을 반복적으로 삭제
		:return:
		"""
		total_cols = self.range_obj.Columns.Count
		if step_on:
			# 반복 삭제 (n, 2n, 3n...)
			current_step = input_no
			while current_step <= total_cols:
				# Columns(n)을 사용하여 해당 열의 값만 지움
				self.range_obj.Columns(current_step).ClearContents()
				current_step += input_no
		else:
			# n번째 한 열만 삭제
			if input_no <= total_cols:
				self.range_obj.Columns(input_no).ClearContents()
			else:
				print(f"경고: 입력한 {input_no}이 영역의 최대 열 수({total_cols})보다 큽니다.")

		# 선택 영역 점선 해제
		self.sheet_obj.Application.CutCopyMode = False
		
