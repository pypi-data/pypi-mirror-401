from pydantic import BaseModel, Field
from typing import Optional, Union

class Model_O1OS9V000880XH10851(BaseModel):
    """Response model for O1OS9V000880XH10851"""
    YR: Union[str, int, float, None] = Field(None, description="연도", alias="YR")
    FST_DIV_ETC: Union[str, int, float, None] = Field(None, description="구분", alias="FST_DIV_ETC")
    SND_DIV_ETC: Union[str, int, float, None] = Field(None, description="구분", alias="SND_DIV_ETC")
    TRD_DIV_ETC: Union[str, int, float, None] = Field(None, description="구분", alias="TRD_DIV_ETC")
    PYM_EXEAMT: Union[str, int, float, None] = Field(None, description="지급액", alias="PYM_EXEAMT")
    PYM_MTH: Union[str, int, float, None] = Field(None, description="지급방법", alias="PYM_MTH")

class Params_O1OS9V000880XH10851(BaseModel):
    """Request parameters for O1OS9V000880XH10851"""
    YR: str | None = Field(None, description="연도", alias="YR")
    FST_DIV_ETC: str | None = Field(None, description="구분", alias="FST_DIV_ETC")
    SND_DIV_ETC: str | None = Field(None, description="구분", alias="SND_DIV_ETC")
    TRD_DIV_ETC: str | None = Field(None, description="구분", alias="TRD_DIV_ETC")
    PYM_MTH: str | None = Field(None, description="지급방법", alias="PYM_MTH")

class Model_OJH286001107IK13829(BaseModel):
    """Response model for OJH286001107IK13829"""
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_OJH286001107IK13829(BaseModel):
    """Request parameters for OJH286001107IK13829"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: str | None = Field(None, description="등록일자", alias="INSERTDT")

class Model_OOWY4R001216HX11519(BaseModel):
    """Response model for OOWY4R001216HX11519"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    CONF_KND: Union[str, int, float, None] = Field(None, description="회의종류", alias="CONF_KND")
    CMIT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="CMIT_CD")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    SB_CMIT_CD: Union[str, int, float, None] = Field(None, description="소위원회코드", alias="SB_CMIT_CD")
    SB_CMIT_NM: Union[str, int, float, None] = Field(None, description="소위원회명", alias="SB_CMIT_NM")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운로드 URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11519(BaseModel):
    """Request parameters for OOWY4R001216HX11519"""
    ERACO: str | None = Field(None, description="대수", alias="ERACO")
    CMIT_CD: str | None = Field(None, description="위원회코드", alias="CMIT_CD")

class Model_O6V35E001197UE12021(BaseModel):
    """Response model for O6V35E001197UE12021"""
    TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="TITLE")
    CHIEF_RESRCH: Union[str, int, float, None] = Field(None, description="연구 책임자", alias="CHIEF_RESRCH")
    REG_DTTM: Union[str, int, float, None] = Field(None, description="작성일", alias="REG_DTTM")
    DETAIL_URL: Union[str, int, float, None] = Field(None, description="상세 URL", alias="DETAIL_URL")

class Params_O6V35E001197UE12021(BaseModel):
    """Request parameters for O6V35E001197UE12021"""
    pass

class Model_OOWY4R001216HX11423(BaseModel):
    """Response model for OOWY4R001216HX11423"""
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    CONF_NM: Union[str, int, float, None] = Field(None, description="회의명", alias="CONF_NM")
    LBRD_STAT: Union[str, int, float, None] = Field(None, description="생중계상태", alias="LBRD_STAT")

class Params_OOWY4R001216HX11423(BaseModel):
    """Request parameters for OOWY4R001216HX11423"""
    pass

class Model_OVRSWG000917L610310(BaseModel):
    """Response model for OVRSWG000917L610310"""
    YR: Union[str, int, float, None] = Field(None, description="년도", alias="YR")
    INST_CD: Union[str, int, float, None] = Field(None, description="기관", alias="INST_CD")
    SN: Union[str, int, float, None] = Field(None, description="일련번호", alias="SN")
    IND_NM: Union[str, int, float, None] = Field(None, description="사건명", alias="IND_NM")
    RSLT_DT: Union[str, int, float, None] = Field(None, description="판결일", alias="RSLT_DT")
    OJ_PN: Union[str, int, float, None] = Field(None, description="피고", alias="OJ_PN")
    ORDG_RSON: Union[str, int, float, None] = Field(None, description="주문내용", alias="ORDG_RSON")
    DEMD_MEAN: Union[str, int, float, None] = Field(None, description="청구취지", alias="DEMD_MEAN")
    RSLT_MTH: Union[str, int, float, None] = Field(None, description="이유(판결요지)", alias="RSLT_MTH")

class Params_OVRSWG000917L610310(BaseModel):
    """Request parameters for OVRSWG000917L610310"""
    YR: str | None = Field(None, description="년도", alias="YR")
    INST_CD: str | None = Field(None, description="기관", alias="INST_CD")
    SN: str | None = Field(None, description="일련번호", alias="SN")
    IND_NM: str | None = Field(None, description="사건명", alias="IND_NM")
    RSLT_DT: str | None = Field(None, description="판결일", alias="RSLT_DT")
    OJ_PN: str | None = Field(None, description="피고", alias="OJ_PN")
    ORDG_RSON: str | None = Field(None, description="주문내용", alias="ORDG_RSON")
    DEMD_MEAN: str | None = Field(None, description="청구취지", alias="DEMD_MEAN")

class Model_OOWY4R001216HX11496(BaseModel):
    """Response model for OOWY4R001216HX11496"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    RCP_CNT: Union[str, int, float, None] = Field(None, description="접수 건수", alias="RCP_CNT")
    ACP_CNT: Union[str, int, float, None] = Field(None, description="채택 건수", alias="ACP_CNT")
    NOT_SUBMIT_CNT: Union[str, int, float, None] = Field(None, description="본회의불부의 건수", alias="NOT_SUBMIT_CNT")
    WTHD_CNT: Union[str, int, float, None] = Field(None, description="철회 건수", alias="WTHD_CNT")
    DSU_CNT: Union[str, int, float, None] = Field(None, description="폐기 건수", alias="DSU_CNT")
    REFT_SUBT: Union[str, int, float, None] = Field(None, description="처리건수 소계", alias="REFT_SUBT")
    NOT_FINISH_CNT: Union[str, int, float, None] = Field(None, description="계류 건수", alias="NOT_FINISH_CNT")

class Params_OOWY4R001216HX11496(BaseModel):
    """Request parameters for OOWY4R001216HX11496"""
    ERACO: str = Field(..., description="대수", alias="ERACO")

class Model_ORL1S4001007HM19790(BaseModel):
    """Response model for ORL1S4001007HM19790"""
    BLNG_INST_NM: Union[str, int, float, None] = Field(None, description="소속기관명", alias="BLNG_INST_NM")
    BRDI_SJ: Union[str, int, float, None] = Field(None, description="제목", alias="BRDI_SJ")
    BRDI_CN: Union[str, int, float, None] = Field(None, description="내용", alias="BRDI_CN")
    RDT: Union[str, int, float, None] = Field(None, description="작성일자", alias="RDT")
    HOME_URL: Union[str, int, float, None] = Field(None, description="바로가기URL", alias="HOME_URL")

class Params_ORL1S4001007HM19790(BaseModel):
    """Request parameters for ORL1S4001007HM19790"""
    BLNG_INST_NM: str | None = Field(None, description="소속기관명", alias="BLNG_INST_NM")
    BRDI_SJ: str | None = Field(None, description="제목", alias="BRDI_SJ")
    BRDI_CN: str | None = Field(None, description="내용", alias="BRDI_CN")
    RDT: str | None = Field(None, description="작성일자", alias="RDT")

class Model_OOWY4R001216HX11497(BaseModel):
    """Response model for OOWY4R001216HX11497"""
    RPT_YR: Union[str, int, float, None] = Field(None, description="보고서 년도", alias="RPT_YR")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    RPT_TTL: Union[str, int, float, None] = Field(None, description="보고서 제목", alias="RPT_TTL")
    PDF_DWLD_URL: Union[str, int, float, None] = Field(None, description="PDF 다운 URL", alias="PDF_DWLD_URL")
    HWP_DWLD_URL: Union[str, int, float, None] = Field(None, description="HWP 다운 URL", alias="HWP_DWLD_URL")

class Params_OOWY4R001216HX11497(BaseModel):
    """Request parameters for OOWY4R001216HX11497"""
    RPT_YR: str | None = Field(None, description="보고서 년도", alias="RPT_YR")
    RPT_TTL: str | None = Field(None, description="보고서 제목", alias="RPT_TTL")

class Model_OU9HJK001126JG15339(BaseModel):
    """Response model for OU9HJK001126JG15339"""
    PRDC_YM_NM: Union[str, int, float, None] = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: Union[str, int, float, None] = Field(None, description="공개파일명", alias="OPB_FL_NM")
    INST_CD: Union[str, int, float, None] = Field(None, description="기관코드", alias="INST_CD")
    INST_NM: Union[str, int, float, None] = Field(None, description="기관명", alias="INST_NM")
    OPB_FL_PH: Union[str, int, float, None] = Field(None, description="공개파일경로", alias="OPB_FL_PH")
    FILE_ID: Union[str, int, float, None] = Field(None, description="파일ID", alias="FILE_ID")

class Params_OU9HJK001126JG15339(BaseModel):
    """Request parameters for OU9HJK001126JG15339"""
    PRDC_YM_NM: str | None = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: str | None = Field(None, description="공개파일명", alias="OPB_FL_NM")

class Model_OOWY4R001216HX11429(BaseModel):
    """Response model for OOWY4R001216HX11429"""
    ARTC_TTL: Union[str, int, float, None] = Field(None, description="행사제목", alias="ARTC_TTL")
    AVDV_START_DT: Union[str, int, float, None] = Field(None, description="행사 시작 일자", alias="AVDV_START_DT")
    AVDV_END_DT: Union[str, int, float, None] = Field(None, description="행사 종료 일자", alias="AVDV_END_DT")
    PLC_NM: Union[str, int, float, None] = Field(None, description="장소명", alias="PLC_NM")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11429(BaseModel):
    """Request parameters for OOWY4R001216HX11429"""
    ARTC_TTL: str | None = Field(None, description="행사제목", alias="ARTC_TTL")

class Model_OOWY4R001216HX11526(BaseModel):
    """Response model for OOWY4R001216HX11526"""
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안 ID", alias="BILL_ID")
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    CONF_KND: Union[str, int, float, None] = Field(None, description="회의 종류", alias="CONF_KND")
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의 ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11526(BaseModel):
    """Request parameters for OOWY4R001216HX11526"""
    BILL_ID: str = Field(..., description="의안 ID", alias="BILL_ID")

class Model_O01TEW000977U011862(BaseModel):
    """Response model for O01TEW000977U011862"""
    V_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="V_TITLE")
    URL_LINK: Union[str, int, float, None] = Field(None, description="기사 URL", alias="URL_LINK")
    DATE_LASTMODIFIED: Union[str, int, float, None] = Field(None, description="최종수정일", alias="DATE_LASTMODIFIED")
    DATE_RELEASED: Union[str, int, float, None] = Field(None, description="기사작성일", alias="DATE_RELEASED")
    V_BODY: Union[str, int, float, None] = Field(None, description="기사내용", alias="V_BODY")

class Params_O01TEW000977U011862(BaseModel):
    """Request parameters for O01TEW000977U011862"""
    V_TITLE: str | None = Field(None, description="제목", alias="V_TITLE")

class Model_OOWY4R001216HX11442(BaseModel):
    """Response model for OOWY4R001216HX11442"""
    FR_LAW_REV_TTL: Union[str, int, float, None] = Field(None, description="해외주요법률 제개정 제목", alias="FR_LAW_REV_TTL")
    WRT_NM: Union[str, int, float, None] = Field(None, description="작성자", alias="WRT_NM")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일자", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11442(BaseModel):
    """Request parameters for OOWY4R001216HX11442"""
    FR_LAW_REV_TTL: str | None = Field(None, description="해외주요법률 제개정 제목", alias="FR_LAW_REV_TTL")

class Model_OQ68B8001071ZB13418(BaseModel):
    """Response model for OQ68B8001071ZB13418"""
    AGE: Union[str, int, float, None] = Field(None, description="대수", alias="AGE")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    BILL_KIND: Union[str, int, float, None] = Field(None, description="의안활동구분", alias="BILL_KIND")
    PROPOSER: Union[str, int, float, None] = Field(None, description="제안자", alias="PROPOSER")
    COMMITTEE_NM: Union[str, int, float, None] = Field(None, description="소관위원회", alias="COMMITTEE_NM")
    PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="의결결과", alias="PROC_RESULT_CD")
    VOTE_TCNT: Union[str, int, float, None] = Field(None, description="총투표수", alias="VOTE_TCNT")
    YES_TCNT: Union[str, int, float, None] = Field(None, description="찬성", alias="YES_TCNT")
    NO_TCNT: Union[str, int, float, None] = Field(None, description="반대", alias="NO_TCNT")
    BLANK_TCNT: Union[str, int, float, None] = Field(None, description="기권", alias="BLANK_TCNT")
    PROPOSE_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PROPOSE_DT")
    COMMITTEE_SUBMIT_DT: Union[str, int, float, None] = Field(None, description="위원회심사_회부일", alias="COMMITTEE_SUBMIT_DT")
    COMMITTEE_PRESENT_DT: Union[str, int, float, None] = Field(None, description="위원회심사_상정일", alias="COMMITTEE_PRESENT_DT")
    COMMITTEE_PROC_DT: Union[str, int, float, None] = Field(None, description="위원회심사_의결일", alias="COMMITTEE_PROC_DT")
    LAW_SUBMIT_DT: Union[str, int, float, None] = Field(None, description="법사위체계자구심사_회부일", alias="LAW_SUBMIT_DT")
    LAW_PRESENT_DT: Union[str, int, float, None] = Field(None, description="법사위체계자구심사_상정일", alias="LAW_PRESENT_DT")
    LAW_PROC_DT: Union[str, int, float, None] = Field(None, description="법사위체계자구심사_의결일", alias="LAW_PROC_DT")
    RGS_PRESENT_DT: Union[str, int, float, None] = Field(None, description="본회의심의_상정일", alias="RGS_PRESENT_DT")
    RGS_PROC_DT: Union[str, int, float, None] = Field(None, description="본회의심의_의결일", alias="RGS_PROC_DT")
    CURR_TRANS_DT: Union[str, int, float, None] = Field(None, description="정부이송일", alias="CURR_TRANS_DT")
    ANNOUNCE_DT: Union[str, int, float, None] = Field(None, description="공포일", alias="ANNOUNCE_DT")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위원회ID", alias="CURR_COMMITTEE_ID")

class Params_OQ68B8001071ZB13418(BaseModel):
    """Request parameters for OQ68B8001071ZB13418"""
    AGE: str = Field(..., description="대수", alias="AGE")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NM: str | None = Field(None, description="의안명", alias="BILL_NM")
    PROPOSER: str | None = Field(None, description="제안자", alias="PROPOSER")
    COMMITTEE_NM: str | None = Field(None, description="소관위원회", alias="COMMITTEE_NM")
    PROC_RESULT_CD: str | None = Field(None, description="의결결과", alias="PROC_RESULT_CD")
    PROPOSE_DT: str | None = Field(None, description="제안일", alias="PROPOSE_DT")
    RGS_PROC_DT: str | None = Field(None, description="본회의심의_의결일", alias="RGS_PROC_DT")
    CURR_TRANS_DT: str | None = Field(None, description="정부이송일", alias="CURR_TRANS_DT")
    ANNOUNCE_DT: str | None = Field(None, description="공포일", alias="ANNOUNCE_DT")
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위원회ID", alias="CURR_COMMITTEE_ID")

class Model_O2U9RG001168QQ15766(BaseModel):
    """Response model for O2U9RG001168QQ15766"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_O2U9RG001168QQ15766(BaseModel):
    """Request parameters for O2U9RG001168QQ15766"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_O575RS001118PF15881(BaseModel):
    """Response model for O575RS001118PF15881"""
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_O575RS001118PF15881(BaseModel):
    """Request parameters for O575RS001118PF15881"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: str | None = Field(None, description="등록일자", alias="INSERTDT")

class Model_OZ2W6L0011539T11384(BaseModel):
    """Response model for OZ2W6L0011539T11384"""
    PRDC_YM_NM: Union[str, int, float, None] = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: Union[str, int, float, None] = Field(None, description="공개파일명", alias="OPB_FL_NM")
    INST_CD: Union[str, int, float, None] = Field(None, description="기관코드", alias="INST_CD")
    INST_NM: Union[str, int, float, None] = Field(None, description="기관명", alias="INST_NM")
    OPB_FL_PH: Union[str, int, float, None] = Field(None, description="공개파일경로", alias="OPB_FL_PH")
    CTGR_CD: Union[str, int, float, None] = Field(None, description="분류항목코드", alias="CTGR_CD")
    CTGR_NM: Union[str, int, float, None] = Field(None, description="분류항목", alias="CTGR_NM")
    FILE_ID: Union[str, int, float, None] = Field(None, description="파일ID", alias="FILE_ID")

class Params_OZ2W6L0011539T11384(BaseModel):
    """Request parameters for OZ2W6L0011539T11384"""
    PRDC_YM_NM: str | None = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: str | None = Field(None, description="공개파일명", alias="OPB_FL_NM")

class Model_O9RY2V0011518716129(BaseModel):
    """Response model for O9RY2V0011518716129"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    LCST_FMLAWMKCT: Union[str, int, float, None] = Field(None, description="지역구여성의원수", alias="LCST_FMLAWMKCT")
    LCST_FMLAWMKNM: Union[str, int, float, None] = Field(None, description="지역구여성의원명", alias="LCST_FMLAWMKNM")
    NATION_FMLAWMKCT: Union[str, int, float, None] = Field(None, description="전국구여성의원수", alias="NATION_FMLAWMKCT")
    NATION_FMLAWMKNM: Union[str, int, float, None] = Field(None, description="전국구여성의원명", alias="NATION_FMLAWMKNM")
    SUM: Union[str, int, float, None] = Field(None, description="합계", alias="SUM")
    RMK: Union[str, int, float, None] = Field(None, description="비고", alias="RMK")

class Params_O9RY2V0011518716129(BaseModel):
    """Request parameters for O9RY2V0011518716129"""
    ERACO: str | None = Field(None, description="대수", alias="ERACO")

class Model_OOWY4R001216HX11444(BaseModel):
    """Response model for OOWY4R001216HX11444"""
    MN_ACTV_TTL: Union[str, int, float, None] = Field(None, description="주요동정 제목", alias="MN_ACTV_TTL")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일자", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11444(BaseModel):
    """Request parameters for OOWY4R001216HX11444"""
    MN_ACTV_TTL: str | None = Field(None, description="주요동정 제목", alias="MN_ACTV_TTL")

class Model_OK7XM1000938DS17215(BaseModel):
    """Response model for OK7XM1000938DS17215"""
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="법률안명", alias="BILL_NAME")
    COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위원회", alias="COMMITTEE")
    PROPOSE_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PROPOSE_DT")
    PROC_RESULT: Union[str, int, float, None] = Field(None, description="본회의심의결과", alias="PROC_RESULT")
    AGE: Union[str, int, float, None] = Field(None, description="대수", alias="AGE")
    DETAIL_LINK: Union[str, int, float, None] = Field(None, description="상세페이지", alias="DETAIL_LINK")
    PROPOSER: Union[str, int, float, None] = Field(None, description="제안자", alias="PROPOSER")
    MEMBER_LIST: Union[str, int, float, None] = Field(None, description="제안자목록링크", alias="MEMBER_LIST")
    LAW_PROC_DT: Union[str, int, float, None] = Field(None, description="법사위처리일", alias="LAW_PROC_DT")
    LAW_PRESENT_DT: Union[str, int, float, None] = Field(None, description="법사위상정일", alias="LAW_PRESENT_DT")
    LAW_SUBMIT_DT: Union[str, int, float, None] = Field(None, description="법사위회부일", alias="LAW_SUBMIT_DT")
    CMT_PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="소관위처리결과", alias="CMT_PROC_RESULT_CD")
    CMT_PROC_DT: Union[str, int, float, None] = Field(None, description="소관위처리일", alias="CMT_PROC_DT")
    CMT_PRESENT_DT: Union[str, int, float, None] = Field(None, description="소관위상정일", alias="CMT_PRESENT_DT")
    COMMITTEE_DT: Union[str, int, float, None] = Field(None, description="소관위회부일", alias="COMMITTEE_DT")
    PROC_DT: Union[str, int, float, None] = Field(None, description="의결일", alias="PROC_DT")
    COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위원회ID", alias="COMMITTEE_ID")
    PUBL_PROPOSER: Union[str, int, float, None] = Field(None, description="공동발의자", alias="PUBL_PROPOSER")
    LAW_PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="법사위처리결과", alias="LAW_PROC_RESULT_CD")
    RST_PROPOSER: Union[str, int, float, None] = Field(None, description="대표발의자", alias="RST_PROPOSER")

class Params_OK7XM1000938DS17215(BaseModel):
    """Request parameters for OK7XM1000938DS17215"""
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: str | None = Field(None, description="법률안명", alias="BILL_NAME")
    COMMITTEE: str | None = Field(None, description="소관위원회", alias="COMMITTEE")
    PROC_RESULT: str | None = Field(None, description="본회의심의결과", alias="PROC_RESULT")
    AGE: str = Field(..., description="대수", alias="AGE")
    PROPOSER: str | None = Field(None, description="제안자", alias="PROPOSER")
    COMMITTEE_ID: str | None = Field(None, description="소관위원회ID", alias="COMMITTEE_ID")

class Model_OJAMPB0011929O11426(BaseModel):
    """Response model for OJAMPB0011929O11426"""
    PRDC_YM_NM: Union[str, int, float, None] = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: Union[str, int, float, None] = Field(None, description="공개파일명", alias="OPB_FL_NM")
    INST_CD: Union[str, int, float, None] = Field(None, description="기관코드", alias="INST_CD")
    INST_NM: Union[str, int, float, None] = Field(None, description="기관명", alias="INST_NM")
    OPB_FL_PH: Union[str, int, float, None] = Field(None, description="공개파일경로", alias="OPB_FL_PH")
    CTGR_CD: Union[str, int, float, None] = Field(None, description="분류항목코드", alias="CTGR_CD")
    CTGR_NM: Union[str, int, float, None] = Field(None, description="분류항목", alias="CTGR_NM")
    FILE_ID: Union[str, int, float, None] = Field(None, description="파일ID", alias="FILE_ID")

class Params_OJAMPB0011929O11426(BaseModel):
    """Request parameters for OJAMPB0011929O11426"""
    PRDC_YM_NM: str | None = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: str | None = Field(None, description="공개파일명", alias="OPB_FL_NM")
    INST_NM: str | None = Field(None, description="기관명", alias="INST_NM")

class Model_O04X68000884BE13083(BaseModel):
    """Response model for O04X68000884BE13083"""
    YR: Union[str, int, float, None] = Field(None, description="연도", alias="YR")
    JBTP_NM: Union[str, int, float, None] = Field(None, description="직류", alias="JBTP_NM")
    ADPT_NOP: Union[str, int, float, None] = Field(None, description="채용인원", alias="ADPT_NOP")
    CMPT_RT: Union[str, int, float, None] = Field(None, description="경쟁률", alias="CMPT_RT")

class Params_O04X68000884BE13083(BaseModel):
    """Request parameters for O04X68000884BE13083"""
    YR: str | None = Field(None, description="연도", alias="YR")
    JBTP_NM: str | None = Field(None, description="직류", alias="JBTP_NM")

class Model_ONVQB00009257H12418(BaseModel):
    """Response model for ONVQB00009257H12418"""
    YR: Union[str, int, float, None] = Field(None, description="년도", alias="YR")
    INST_NM: Union[str, int, float, None] = Field(None, description="기관명", alias="INST_NM")
    BDG_TAMT: Union[str, int, float, None] = Field(None, description="예산총액", alias="BDG_TAMT")

class Params_ONVQB00009257H12418(BaseModel):
    """Request parameters for ONVQB00009257H12418"""
    YR: str | None = Field(None, description="년도", alias="YR")
    INST_NM: str | None = Field(None, description="기관명", alias="INST_NM")

class Model_O4UN9N000961PS11812(BaseModel):
    """Response model for O4UN9N000961PS11812"""
    MEETING_DATE: Union[str, int, float, None] = Field(None, description="회의일자", alias="MEETING_DATE")
    MEETING_TIME: Union[str, int, float, None] = Field(None, description="시간", alias="MEETING_TIME")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DEGREE: Union[str, int, float, None] = Field(None, description="차수", alias="DEGREE")
    TITLE: Union[str, int, float, None] = Field(None, description="구분", alias="TITLE")
    COMMITTEE_NAME: Union[str, int, float, None] = Field(None, description="위원회 명", alias="COMMITTEE_NAME")
    LINK_URL2: Union[str, int, float, None] = Field(None, description="상세_URL", alias="LINK_URL2")
    UNIT_CD: Union[str, int, float, None] = Field(None, description="대수", alias="UNIT_CD")
    UNIT_NM: Union[str, int, float, None] = Field(None, description="대수", alias="UNIT_NM")
    HR_DEPT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="HR_DEPT_CD")
    ANGUN: Union[str, int, float, None] = Field(None, description="안건", alias="ANGUN")

class Params_O4UN9N000961PS11812(BaseModel):
    """Request parameters for O4UN9N000961PS11812"""
    MEETING_DATE: str | None = Field(None, description="회의일자", alias="MEETING_DATE")
    MEETING_TIME: str | None = Field(None, description="시간", alias="MEETING_TIME")
    SESS: str | None = Field(None, description="회기", alias="SESS")
    DEGREE: str | None = Field(None, description="차수", alias="DEGREE")
    TITLE: str | None = Field(None, description="구분", alias="TITLE")
    COMMITTEE_NAME: str | None = Field(None, description="위원회 명", alias="COMMITTEE_NAME")
    UNIT_CD: str = Field(..., description="대수", alias="UNIT_CD")
    HR_DEPT_CD: str | None = Field(None, description="위원회코드", alias="HR_DEPT_CD")

class Model_OOWY4R001216HX11493(BaseModel):
    """Response model for OOWY4R001216HX11493"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    PPSR: Union[str, int, float, None] = Field(None, description="제안자", alias="PPSR")
    PPSL_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PPSL_DT")
    LWCMIT_CONF_NM: Union[str, int, float, None] = Field(None, description="법사위 회의명", alias="LWCMIT_CONF_NM")
    LWCMIT_CONF_DT: Union[str, int, float, None] = Field(None, description="법사위 회의일", alias="LWCMIT_CONF_DT")
    LWCMIT_CONF_RSLT: Union[str, int, float, None] = Field(None, description="법사위 회의결과", alias="LWCMIT_CONF_RSLT")

class Params_OOWY4R001216HX11493(BaseModel):
    """Request parameters for OOWY4R001216HX11493"""
    BILL_ID: str = Field(..., description="의안ID", alias="BILL_ID")

class Model_OQEXW00012074114927(BaseModel):
    """Response model for OQEXW00012074114927"""
    DATA_SEQCE_NO: Union[str, int, float, None] = Field(None, description="데이터수집번호", alias="DATA_SEQCE_NO")
    DATAID: Union[str, int, float, None] = Field(None, description="데이터ID", alias="DATAID")
    PDFFILENM: Union[str, int, float, None] = Field(None, description="다운로드", alias="PDFFILENM")
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    DIRECTVIEW: Union[str, int, float, None] = Field(None, description="바로보기", alias="DIRECTVIEW")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    DIVNM: Union[str, int, float, None] = Field(None, description="구분명", alias="DIVNM")
    DIVCD: Union[str, int, float, None] = Field(None, description="구분코드", alias="DIVCD")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_OQEXW00012074114927(BaseModel):
    """Request parameters for OQEXW00012074114927"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")

class Model_OG88RA000978S210177(BaseModel):
    """Response model for OG88RA000978S210177"""
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    AGE: Union[str, int, float, None] = Field(None, description="대수", alias="AGE")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NAME")
    PROPOSER: Union[str, int, float, None] = Field(None, description="제안자", alias="PROPOSER")
    PROPOSER_KIND: Union[str, int, float, None] = Field(None, description="제안자구분", alias="PROPOSER_KIND")
    PROPOSE_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PROPOSE_DT")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위", alias="CURR_COMMITTEE")
    COMMITTEE_DT: Union[str, int, float, None] = Field(None, description="소관위회부일", alias="COMMITTEE_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="의안상세정보 URL", alias="LINK_URL")
    COMMITTEE_RESULT: Union[str, int, float, None] = Field(None, description="소관위처리결과", alias="COMMITTEE_RESULT")
    COMMITTEE_PROC_DT: Union[str, int, float, None] = Field(None, description="소관위처리일", alias="COMMITTEE_PROC_DT")
    CMT_PRESENT_DT: Union[str, int, float, None] = Field(None, description="소관위상정일", alias="CMT_PRESENT_DT")
    LAW_SUBMIT_DT: Union[str, int, float, None] = Field(None, description="법사위회부일", alias="LAW_SUBMIT_DT")
    LAW_PRESENT_DT: Union[str, int, float, None] = Field(None, description="법사위상정일", alias="LAW_PRESENT_DT")

class Params_OG88RA000978S210177(BaseModel):
    """Request parameters for OG88RA000978S210177"""
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: str | None = Field(None, description="의안명", alias="BILL_NAME")
    PROPOSER: str | None = Field(None, description="제안자", alias="PROPOSER")
    PROPOSE_DT: str | None = Field(None, description="제안일", alias="PROPOSE_DT")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: str | None = Field(None, description="소관위", alias="CURR_COMMITTEE")

class Model_OAUJIX001138TP16525(BaseModel):
    """Response model for OAUJIX001138TP16525"""
    ARTICLE_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="ARTICLE_TITLE")
    CATEGORY_NM: Union[str, int, float, None] = Field(None, description="대수", alias="CATEGORY_NM")
    ETC_CHAR7: Union[str, int, float, None] = Field(None, description="국회의원", alias="ETC_CHAR7")
    ETC_CHAR12: Union[str, int, float, None] = Field(None, description="개최장소", alias="ETC_CHAR12")
    LINK_URL: Union[str, int, float, None] = Field(None, description="상세보기URL", alias="LINK_URL")
    ETC_CHAR1: Union[str, int, float, None] = Field(None, description="개최일", alias="ETC_CHAR1")
    ETC_CHAR2: Union[str, int, float, None] = Field(None, description="개최시", alias="ETC_CHAR2")

class Params_OAUJIX001138TP16525(BaseModel):
    """Request parameters for OAUJIX001138TP16525"""
    ARTICLE_TITLE: str | None = Field(None, description="제목", alias="ARTICLE_TITLE")
    CATEGORY_NM: str | None = Field(None, description="대수", alias="CATEGORY_NM")
    ETC_CHAR7: str | None = Field(None, description="국회의원", alias="ETC_CHAR7")
    ETC_CHAR12: str | None = Field(None, description="개최장소", alias="ETC_CHAR12")

class Model_OCROAA001181NA17461(BaseModel):
    """Response model for OCROAA001181NA17461"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_OCROAA001181NA17461(BaseModel):
    """Request parameters for OCROAA001181NA17461"""
    REG_DATE: str | None = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_O2QQLK001176HI14481(BaseModel):
    """Response model for O2QQLK001176HI14481"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_O2QQLK001176HI14481(BaseModel):
    """Request parameters for O2QQLK001176HI14481"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_OOWY4R001216HX11450(BaseModel):
    """Response model for OOWY4R001216HX11450"""
    MTR_DIV: Union[str, int, float, None] = Field(None, description="발간자료구분", alias="MTR_DIV")
    MTR_TTL: Union[str, int, float, None] = Field(None, description="발간자료제목", alias="MTR_TTL")
    PUBLCO_NM: Union[str, int, float, None] = Field(None, description="출판사", alias="PUBLCO_NM")
    PUBLCO_YEAR: Union[str, int, float, None] = Field(None, description="출판년도", alias="PUBLCO_YEAR")
    AUT_NM: Union[str, int, float, None] = Field(None, description="담당자", alias="AUT_NM")
    FRUM_PANL_NM: Union[str, int, float, None] = Field(None, description="미래포럼 패널", alias="FRUM_PANL_NM")
    FRUM_OPB_DT: Union[str, int, float, None] = Field(None, description="미래포럼 개최일", alias="FRUM_OPB_DT")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11450(BaseModel):
    """Request parameters for OOWY4R001216HX11450"""
    MTR_DIV: str | None = Field(None, description="발간자료구분", alias="MTR_DIV")
    MTR_TTL: str | None = Field(None, description="발간자료제목", alias="MTR_TTL")

class Model_OVA33G0011172J17084(BaseModel):
    """Response model for OVA33G0011172J17084"""
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_OVA33G0011172J17084(BaseModel):
    """Request parameters for OVA33G0011172J17084"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")

class Model_OVRNQQ001062CO16787(BaseModel):
    """Response model for OVRNQQ001062CO16787"""
    COMP_MAIN_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="COMP_MAIN_TITLE")
    REG_DATE: Union[str, int, float, None] = Field(None, description="등록일자", alias="REG_DATE")
    COMP_CONTENT: Union[str, int, float, None] = Field(None, description="내용", alias="COMP_CONTENT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="상세보기", alias="LINK_URL")

class Params_OVRNQQ001062CO16787(BaseModel):
    """Request parameters for OVRNQQ001062CO16787"""
    COMP_MAIN_TITLE: str | None = Field(None, description="제목", alias="COMP_MAIN_TITLE")
    REG_DATE: str | None = Field(None, description="등록일자", alias="REG_DATE")
    COMP_CONTENT: str | None = Field(None, description="내용", alias="COMP_CONTENT")

class Model_O93OTI000979JV17987(BaseModel):
    """Response model for O93OTI000979JV17987"""
    V_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="V_TITLE")
    URL_LINK: Union[str, int, float, None] = Field(None, description="기사 URL", alias="URL_LINK")
    DATE_LASTMODIFIED: Union[str, int, float, None] = Field(None, description="최종수정일", alias="DATE_LASTMODIFIED")
    DATE_RELEASED: Union[str, int, float, None] = Field(None, description="기사작성일", alias="DATE_RELEASED")
    V_BODY: Union[str, int, float, None] = Field(None, description="기사내용", alias="V_BODY")

class Params_O93OTI000979JV17987(BaseModel):
    """Request parameters for O93OTI000979JV17987"""
    V_TITLE: str | None = Field(None, description="제목", alias="V_TITLE")

class Model_OOWY4R001216HX11454(BaseModel):
    """Response model for OOWY4R001216HX11454"""
    ARTC_TTL: Union[str, int, float, None] = Field(None, description="보도자료 제목", alias="ARTC_TTL")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일자", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11454(BaseModel):
    """Request parameters for OOWY4R001216HX11454"""
    ARTC_TTL: str | None = Field(None, description="보도자료 제목", alias="ARTC_TTL")

class Model_OWSSC6001134T516707(BaseModel):
    """Response model for OWSSC6001134T516707"""
    HG_NM: Union[str, int, float, None] = Field(None, description="이름", alias="HG_NM")
    HJ_NM: Union[str, int, float, None] = Field(None, description="한자명", alias="HJ_NM")
    ENG_NM: Union[str, int, float, None] = Field(None, description="영문명칭", alias="ENG_NM")
    BTH_GBN_NM: Union[str, int, float, None] = Field(None, description="음/양력", alias="BTH_GBN_NM")
    BTH_DATE: Union[str, int, float, None] = Field(None, description="생년월일", alias="BTH_DATE")
    JOB_RES_NM: Union[str, int, float, None] = Field(None, description="직책명", alias="JOB_RES_NM")
    POLY_NM: Union[str, int, float, None] = Field(None, description="정당명", alias="POLY_NM")
    ORIG_NM: Union[str, int, float, None] = Field(None, description="선거구", alias="ORIG_NM")
    ELECT_GBN_NM: Union[str, int, float, None] = Field(None, description="선거구구분", alias="ELECT_GBN_NM")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="대표 위원회", alias="CMIT_NM")
    CMITS: Union[str, int, float, None] = Field(None, description="소속 위원회 목록", alias="CMITS")
    REELE_GBN_NM: Union[str, int, float, None] = Field(None, description="재선", alias="REELE_GBN_NM")
    UNITS: Union[str, int, float, None] = Field(None, description="당선", alias="UNITS")
    SEX_GBN_NM: Union[str, int, float, None] = Field(None, description="성별", alias="SEX_GBN_NM")
    TEL_NO: Union[str, int, float, None] = Field(None, description="전화번호", alias="TEL_NO")
    E_MAIL: Union[str, int, float, None] = Field(None, description="이메일", alias="E_MAIL")
    HOMEPAGE: Union[str, int, float, None] = Field(None, description="홈페이지", alias="HOMEPAGE")
    STAFF: Union[str, int, float, None] = Field(None, description="보좌관", alias="STAFF")
    SECRETARY: Union[str, int, float, None] = Field(None, description="선임비서관", alias="SECRETARY")
    SECRETARY2: Union[str, int, float, None] = Field(None, description="비서관", alias="SECRETARY2")
    MONA_CD: Union[str, int, float, None] = Field(None, description="국회의원코드", alias="MONA_CD")
    MEM_TITLE: Union[str, int, float, None] = Field(None, description="약력", alias="MEM_TITLE")
    ASSEM_ADDR: Union[str, int, float, None] = Field(None, description="사무실 호실", alias="ASSEM_ADDR")

class Params_OWSSC6001134T516707(BaseModel):
    """Request parameters for OWSSC6001134T516707"""
    HG_NM: str | None = Field(None, description="이름", alias="HG_NM")
    POLY_NM: str | None = Field(None, description="정당명", alias="POLY_NM")
    ORIG_NM: str | None = Field(None, description="선거구", alias="ORIG_NM")
    CMITS: str | None = Field(None, description="소속 위원회 목록", alias="CMITS")
    SEX_GBN_NM: str | None = Field(None, description="성별", alias="SEX_GBN_NM")
    MONA_CD: str | None = Field(None, description="국회의원코드", alias="MONA_CD")

class Model_OOWY4R001216HX11419(BaseModel):
    """Response model for OOWY4R001216HX11419"""
    BRDI_TTL: Union[str, int, float, None] = Field(None, description="행사개최결과 제목", alias="BRDI_TTL")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 URL", alias="LINK_URL")

class Params_OOWY4R001216HX11419(BaseModel):
    """Request parameters for OOWY4R001216HX11419"""
    BRDI_TTL: str | None = Field(None, description="행사개최결과 제목", alias="BRDI_TTL")

class Model_OO1X9P001017YF13038(BaseModel):
    """Response model for OO1X9P001017YF13038"""
    CONFER_NUM: Union[str, int, float, None] = Field(None, description="회의번호", alias="CONFER_NUM")
    TITLE: Union[str, int, float, None] = Field(None, description="회의명", alias="TITLE")
    CLASS_NAME: Union[str, int, float, None] = Field(None, description="회의종류명", alias="CLASS_NAME")
    DAE_NUM: Union[str, int, float, None] = Field(None, description="대수", alias="DAE_NUM")
    CONF_DATE: Union[str, int, float, None] = Field(None, description="회의날짜", alias="CONF_DATE")
    SUB_NAME: Union[str, int, float, None] = Field(None, description="안건명", alias="SUB_NAME")
    VOD_LINK_URL: Union[str, int, float, None] = Field(None, description="영상회의록 링크", alias="VOD_LINK_URL")
    CONF_LINK_URL: Union[str, int, float, None] = Field(None, description="요약정보 팝업", alias="CONF_LINK_URL")
    PDF_LINK_URL: Union[str, int, float, None] = Field(None, description="PDF파일 링크", alias="PDF_LINK_URL")
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")

class Params_OO1X9P001017YF13038(BaseModel):
    """Request parameters for OO1X9P001017YF13038"""
    TITLE: str | None = Field(None, description="회의명", alias="TITLE")
    CLASS_NAME: str | None = Field(None, description="회의종류명", alias="CLASS_NAME")
    DAE_NUM: str = Field(..., description="대수", alias="DAE_NUM")
    CONF_DATE: str = Field(..., description="회의날짜", alias="CONF_DATE")
    SUB_NUM: str | None = Field(None, description="안건번호", alias="SUB_NUM")
    SUB_NAME: str | None = Field(None, description="안건명", alias="SUB_NAME")

class Model_OX4XHR001211RB17826(BaseModel):
    """Response model for OX4XHR001211RB17826"""
    TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="TITLE")
    WRITER: Union[str, int, float, None] = Field(None, description="작성자", alias="WRITER")
    REG_DTTM: Union[str, int, float, None] = Field(None, description="작성일", alias="REG_DTTM")
    DETAIL_URL: Union[str, int, float, None] = Field(None, description="상세 URL", alias="DETAIL_URL")

class Params_OX4XHR001211RB17826(BaseModel):
    """Request parameters for OX4XHR001211RB17826"""
    TITLE: str | None = Field(None, description="제목", alias="TITLE")
    WRITER: str | None = Field(None, description="작성자", alias="WRITER")

class Model_OB61LZ000981FC12253(BaseModel):
    """Response model for OB61LZ000981FC12253"""
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    AGE: Union[str, int, float, None] = Field(None, description="대수", alias="AGE")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NAME")
    PROPOSER: Union[str, int, float, None] = Field(None, description="제안자", alias="PROPOSER")
    PROPOSER_KIND: Union[str, int, float, None] = Field(None, description="제안자구분", alias="PROPOSER_KIND")
    PROPOSE_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PROPOSE_DT")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위", alias="CURR_COMMITTEE")
    COMMITTEE_DT: Union[str, int, float, None] = Field(None, description="소관위회부일", alias="COMMITTEE_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="의안상세정보_URL", alias="LINK_URL")
    CMT_PROC_DT: Union[str, int, float, None] = Field(None, description="소관위처리일", alias="CMT_PROC_DT")
    CMT_PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="소관위처리결과", alias="CMT_PROC_RESULT_CD")
    RST_MONA_CD: Union[str, int, float, None] = Field(None, description="대표발의자코드", alias="RST_MONA_CD")
    LAW_PRESENT_DT: Union[str, int, float, None] = Field(None, description="법사위상정일", alias="LAW_PRESENT_DT")
    LAW_PROC_DT: Union[str, int, float, None] = Field(None, description="법사위처리일", alias="LAW_PROC_DT")
    LAW_PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="법사위처리결과", alias="LAW_PROC_RESULT_CD")
    RST_PROPOSER: Union[str, int, float, None] = Field(None, description="대표발의자", alias="RST_PROPOSER")
    CMT_PRESENT_DT: Union[str, int, float, None] = Field(None, description="소관위상정일", alias="CMT_PRESENT_DT")
    LAW_SUBMIT_DT: Union[str, int, float, None] = Field(None, description="법사위회부일", alias="LAW_SUBMIT_DT")

class Params_OB61LZ000981FC12253(BaseModel):
    """Request parameters for OB61LZ000981FC12253"""
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: str | None = Field(None, description="의안명", alias="BILL_NAME")
    PROPOSER: str | None = Field(None, description="제안자", alias="PROPOSER")
    PROPOSER_KIND: str | None = Field(None, description="제안자구분", alias="PROPOSER_KIND")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: str | None = Field(None, description="소관위", alias="CURR_COMMITTEE")

class Model_OJ2LTJ001101KO19739(BaseModel):
    """Response model for OJ2LTJ001101KO19739"""
    TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="TITLE")
    PUBLISHER: Union[str, int, float, None] = Field(None, description="발행처", alias="PUBLISHER")
    DETAIL_VIEW_URL: Union[str, int, float, None] = Field(None, description="상세보기URL", alias="DETAIL_VIEW_URL")
    UPDATE_DT: Union[str, int, float, None] = Field(None, description="수정일", alias="UPDATE_DT")
    PUBLISH_DT: Union[str, int, float, None] = Field(None, description="발행년", alias="PUBLISH_DT")

class Params_OJ2LTJ001101KO19739(BaseModel):
    """Request parameters for OJ2LTJ001101KO19739"""
    TITLE: str | None = Field(None, description="제목", alias="TITLE")
    PUBLISHER: str | None = Field(None, description="발행처", alias="PUBLISHER")
    PUBLISH_DT: str | None = Field(None, description="발행년", alias="PUBLISH_DT")

class Model_OF8AJV000972OP11430(BaseModel):
    """Response model for OF8AJV000972OP11430"""
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안 ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="법률안명", alias="BILL_NAME")
    AGE: Union[str, int, float, None] = Field(None, description="대", alias="AGE")
    PROPOSER_KIND_CD: Union[str, int, float, None] = Field(None, description="제안자구분", alias="PROPOSER_KIND_CD")
    PROPOSER: Union[str, int, float, None] = Field(None, description="제안자", alias="PROPOSER")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위원회", alias="CURR_COMMITTEE")
    NOTI_ED_DT: Union[str, int, float, None] = Field(None, description="게시종료일", alias="NOTI_ED_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크주소", alias="LINK_URL")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위ID", alias="CURR_COMMITTEE_ID")

class Params_OF8AJV000972OP11430(BaseModel):
    """Request parameters for OF8AJV000972OP11430"""
    BILL_ID: str | None = Field(None, description="의안 ID", alias="BILL_ID")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: str | None = Field(None, description="법률안명", alias="BILL_NAME")
    AGE: str = Field(..., description="대", alias="AGE")
    PROPOSER_KIND_CD: str | None = Field(None, description="제안자구분", alias="PROPOSER_KIND_CD")
    PROPOSER: str | None = Field(None, description="제안자", alias="PROPOSER")
    CURR_COMMITTEE: str | None = Field(None, description="소관위원회", alias="CURR_COMMITTEE")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위ID", alias="CURR_COMMITTEE_ID")

class Model_OCSMEJ000953O916134(BaseModel):
    """Response model for OCSMEJ000953O916134"""
    ADD_DISCRIPT: Union[str, int, float, None] = Field(None, description="부제", alias="ADD_DISCRIPT")
    PRO_TITLE: Union[str, int, float, None] = Field(None, description="방송프로그램", alias="PRO_TITLE")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크", alias="LINK_URL")
    FORMATION_TIME: Union[str, int, float, None] = Field(None, description="방영시간", alias="FORMATION_TIME")
    FORMATION_DT: Union[str, int, float, None] = Field(None, description="방영일자", alias="FORMATION_DT")

class Params_OCSMEJ000953O916134(BaseModel):
    """Request parameters for OCSMEJ000953O916134"""
    ADD_DISCRIPT: str | None = Field(None, description="부제", alias="ADD_DISCRIPT")
    PRO_TITLE: str | None = Field(None, description="방송프로그램", alias="PRO_TITLE")
    FORMATION_TIME: str | None = Field(None, description="방영시간", alias="FORMATION_TIME")
    FORMATION_DT: str = Field(..., description="방영일자", alias="FORMATION_DT")

class Model_OOWY4R001216HX11468(BaseModel):
    """Response model for OOWY4R001216HX11468"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    PPSR_KIND: Union[str, int, float, None] = Field(None, description="제안자구분", alias="PPSR_KIND")
    PPSL_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PPSL_DT")
    BDG_CMIT_NM: Union[str, int, float, None] = Field(None, description="예결위심사 위원회명", alias="BDG_CMIT_NM")
    BDG_CMMT_DT: Union[str, int, float, None] = Field(None, description="예결위심사 회부일", alias="BDG_CMMT_DT")
    BDG_PRSNT_DT: Union[str, int, float, None] = Field(None, description="예결위심사 상정일", alias="BDG_PRSNT_DT")
    BDG_RSLN_DT: Union[str, int, float, None] = Field(None, description="예결위심사 의결일", alias="BDG_RSLN_DT")
    BDG_PROC_RSLT: Union[str, int, float, None] = Field(None, description="예결위심사 처리결과", alias="BDG_PROC_RSLT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11468(BaseModel):
    """Request parameters for OOWY4R001216HX11468"""
    ERACO: str | None = Field(None, description="대수", alias="ERACO")

class Model_OGM9FC001165FS12631(BaseModel):
    """Response model for OGM9FC001165FS12631"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_OGM9FC001165FS12631(BaseModel):
    """Request parameters for OGM9FC001165FS12631"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_O2Q4ZT001004PV11014(BaseModel):
    """Response model for O2Q4ZT001004PV11014"""
    CMT_DIV_CD: Union[str, int, float, None] = Field(None, description="위원회구분코드", alias="CMT_DIV_CD")
    CMT_DIV_NM: Union[str, int, float, None] = Field(None, description="위원회구분", alias="CMT_DIV_NM")
    HR_DEPT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="HR_DEPT_CD")
    COMMITTEE_NAME: Union[str, int, float, None] = Field(None, description="위원회", alias="COMMITTEE_NAME")
    HG_NM: Union[str, int, float, None] = Field(None, description="위원장", alias="HG_NM")
    HG_NM_LIST: Union[str, int, float, None] = Field(None, description="간사", alias="HG_NM_LIST")
    LIMIT_CNT: Union[str, int, float, None] = Field(None, description="위원정수", alias="LIMIT_CNT")
    CURR_CNT: Union[str, int, float, None] = Field(None, description="현원", alias="CURR_CNT")
    POLY99_CNT: Union[str, int, float, None] = Field(None, description="비교섭단체위원수", alias="POLY99_CNT")
    POLY_CNT: Union[str, int, float, None] = Field(None, description="교섭단체위원수", alias="POLY_CNT")

class Params_O2Q4ZT001004PV11014(BaseModel):
    """Request parameters for O2Q4ZT001004PV11014"""
    CMT_DIV_NM: str | None = Field(None, description="위원회구분", alias="CMT_DIV_NM")
    HR_DEPT_CD: str | None = Field(None, description="위원회코드", alias="HR_DEPT_CD")
    COMMITTEE_NAME: str | None = Field(None, description="위원회", alias="COMMITTEE_NAME")
    HG_NM: str | None = Field(None, description="위원장", alias="HG_NM")
    HG_NM_LIST: str | None = Field(None, description="간사", alias="HG_NM_LIST")

class Model_O6PTDW000886NN18676(BaseModel):
    """Response model for O6PTDW000886NN18676"""
    YR: Union[str, int, float, None] = Field(None, description="연도", alias="YR")
    JGRD_NM: Union[str, int, float, None] = Field(None, description="직급", alias="JGRD_NM")
    JBTP_NM: Union[str, int, float, None] = Field(None, description="직류", alias="JBTP_NM")
    ADPT_NOP: Union[str, int, float, None] = Field(None, description="채용인원(명)", alias="ADPT_NOP")
    CMPT_RT: Union[str, int, float, None] = Field(None, description="경쟁률", alias="CMPT_RT")

class Params_O6PTDW000886NN18676(BaseModel):
    """Request parameters for O6PTDW000886NN18676"""
    YR: str | None = Field(None, description="연도", alias="YR")
    JGRD_NM: str | None = Field(None, description="직급", alias="JGRD_NM")
    JBTP_NM: str | None = Field(None, description="직류", alias="JBTP_NM")

class Model_ORDPSW001070QH19059(BaseModel):
    """Response model for ORDPSW001070QH19059"""
    MEETINGSESSION: Union[str, int, float, None] = Field(None, description="회기", alias="MEETINGSESSION")
    CHA: Union[str, int, float, None] = Field(None, description="차수", alias="CHA")
    TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="TITLE")
    MEETTING_DATE: Union[str, int, float, None] = Field(None, description="일자", alias="MEETTING_DATE")
    MEETTING_TIME: Union[str, int, float, None] = Field(None, description="일시", alias="MEETTING_TIME")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크주소", alias="LINK_URL")
    UNIT_CD: Union[str, int, float, None] = Field(None, description="대수", alias="UNIT_CD")
    UNIT_NM: Union[str, int, float, None] = Field(None, description="대수", alias="UNIT_NM")
    CONTS: Union[str, int, float, None] = Field(None, description="안건정보", alias="CONTS")

class Params_ORDPSW001070QH19059(BaseModel):
    """Request parameters for ORDPSW001070QH19059"""
    MEETINGSESSION: str | None = Field(None, description="회기", alias="MEETINGSESSION")
    CHA: str | None = Field(None, description="차수", alias="CHA")
    TITLE: str | None = Field(None, description="제목", alias="TITLE")
    MEETTING_DATE: str | None = Field(None, description="일자", alias="MEETTING_DATE")
    UNIT_CD: str = Field(..., description="대수", alias="UNIT_CD")

class Model_OOWY4R001216HX11509(BaseModel):
    """Response model for OOWY4R001216HX11509"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    CONF_KND: Union[str, int, float, None] = Field(None, description="회의종류", alias="CONF_KND")
    CMIT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="CMIT_CD")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운로드 URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11509(BaseModel):
    """Request parameters for OOWY4R001216HX11509"""
    ERACO: str = Field(..., description="대수", alias="ERACO")
    CMIT_CD: str | None = Field(None, description="위원회코드", alias="CMIT_CD")

class Model_O5C2PY001120OH19574(BaseModel):
    """Response model for O5C2PY001120OH19574"""
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_O5C2PY001120OH19574(BaseModel):
    """Request parameters for O5C2PY001120OH19574"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: str | None = Field(None, description="등록일자", alias="INSERTDT")

class Model_O0KGG20011857W15853(BaseModel):
    """Response model for O0KGG20011857W15853"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    ETC_CATE2: Union[str, int, float, None] = Field(None, description="분야", alias="ETC_CATE2")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_O0KGG20011857W15853(BaseModel):
    """Request parameters for O0KGG20011857W15853"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_OA8HOU000969OM19602(BaseModel):
    """Response model for OA8HOU000969OM19602"""
    EDU_TITLE_NM: Union[str, int, float, None] = Field(None, description="연수명", alias="EDU_TITLE_NM")
    EDU_OJR: Union[str, int, float, None] = Field(None, description="대상자", alias="EDU_OJR")
    EDU_PLC_NM: Union[str, int, float, None] = Field(None, description="장소", alias="EDU_PLC_NM")
    EDU_GUBUN_CD: Union[str, int, float, None] = Field(None, description="교육_대상자_구분코드", alias="EDU_GUBUN_CD")
    EDU_GUBUN_NM: Union[str, int, float, None] = Field(None, description="대상구분명", alias="EDU_GUBUN_NM")
    EDU_FXDNOPPL: Union[str, int, float, None] = Field(None, description="정원", alias="EDU_FXDNOPPL")
    CRT_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="CRT_DT")
    EDU_DT: Union[str, int, float, None] = Field(None, description="연수기간", alias="EDU_DT")
    EDU_APL_DT: Union[str, int, float, None] = Field(None, description="신청기간", alias="EDU_APL_DT")
    EDU_APL_CNC_DT: Union[str, int, float, None] = Field(None, description="취소가능기간", alias="EDU_APL_CNC_DT")
    EDU_INQ_CNT: Union[str, int, float, None] = Field(None, description="조회수", alias="EDU_INQ_CNT")

class Params_OA8HOU000969OM19602(BaseModel):
    """Request parameters for OA8HOU000969OM19602"""
    EDU_TITLE_NM: str | None = Field(None, description="연수명", alias="EDU_TITLE_NM")
    EDU_OJR: str | None = Field(None, description="대상자", alias="EDU_OJR")
    EDU_PLC_NM: str | None = Field(None, description="장소", alias="EDU_PLC_NM")
    EDU_GUBUN_NM: str | None = Field(None, description="대상구분명", alias="EDU_GUBUN_NM")
    EDU_DT: str | None = Field(None, description="연수기간", alias="EDU_DT")

class Model_O0UBVR000906UG11689(BaseModel):
    """Response model for O0UBVR000906UG11689"""
    YR: Union[str, int, float, None] = Field(None, description="년도", alias="YR")
    SN: Union[str, int, float, None] = Field(None, description="일련번호", alias="SN")
    DEMD_RSON: Union[str, int, float, None] = Field(None, description="청구사항>청구내용", alias="DEMD_RSON")
    OPB_FOM_NM: Union[str, int, float, None] = Field(None, description="청구사항>공개형태", alias="OPB_FOM_NM")
    CHRG_DEPT_NM: Union[str, int, float, None] = Field(None, description="결정내용>담당부서", alias="CHRG_DEPT_NM")
    DCS_DIV: Union[str, int, float, None] = Field(None, description="결정내용>결정구분", alias="DCS_DIV")
    OPB_RSON: Union[str, int, float, None] = Field(None, description="결정내용>공개내용", alias="OPB_RSON")
    CLSD_RSON: Union[str, int, float, None] = Field(None, description="결정내용>비공개(부분공개) 내용 및 사유", alias="CLSD_RSON")
    DCS_NTC_DT: Union[str, int, float, None] = Field(None, description="결정내용>결정통지일자", alias="DCS_NTC_DT")
    OPB_DT: Union[str, int, float, None] = Field(None, description="처리사항>공개일자", alias="OPB_DT")
    OPB_MTH: Union[str, int, float, None] = Field(None, description="처리사항>공개방법", alias="OPB_MTH")

class Params_O0UBVR000906UG11689(BaseModel):
    """Request parameters for O0UBVR000906UG11689"""
    YR: str | None = Field(None, description="년도", alias="YR")
    SN: str | None = Field(None, description="일련번호", alias="SN")
    DEMD_RSON: str | None = Field(None, description="청구사항>청구내용", alias="DEMD_RSON")
    OPB_FOM_NM: str | None = Field(None, description="청구사항>공개형태", alias="OPB_FOM_NM")
    CHRG_DEPT_NM: str | None = Field(None, description="결정내용>담당부서", alias="CHRG_DEPT_NM")
    DCS_DIV: str | None = Field(None, description="결정내용>결정구분", alias="DCS_DIV")
    OPB_RSON: str | None = Field(None, description="결정내용>공개내용", alias="OPB_RSON")
    CLSD_RSON: str | None = Field(None, description="결정내용>비공개(부분공개) 내용 및 사유", alias="CLSD_RSON")
    DCS_NTC_DT: str | None = Field(None, description="결정내용>결정통지일자", alias="DCS_NTC_DT")

class Model_OD0T6I001156CA16296(BaseModel):
    """Response model for OD0T6I001156CA16296"""
    TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="TITLE")
    SYSATTACH1: Union[str, int, float, None] = Field(None, description="파일링크", alias="SYSATTACH1")
    REG_DATE: Union[str, int, float, None] = Field(None, description="등록일자", alias="REG_DATE")

class Params_OD0T6I001156CA16296(BaseModel):
    """Request parameters for OD0T6I001156CA16296"""
    TITLE: str | None = Field(None, description="제목", alias="TITLE")

class Model_OZN379001174FW17905(BaseModel):
    """Response model for OZN379001174FW17905"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_OZN379001174FW17905(BaseModel):
    """Request parameters for OZN379001174FW17905"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_OOWY4R001216HX11425(BaseModel):
    """Response model for OOWY4R001216HX11425"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    PTT_NO: Union[str, int, float, None] = Field(None, description="청원번호", alias="PTT_NO")
    PTT_TTL: Union[str, int, float, None] = Field(None, description="청원제목", alias="PTT_TTL")
    PTTR_NM: Union[str, int, float, None] = Field(None, description="청원자명", alias="PTTR_NM")
    INTD_ASBLM_NM: Union[str, int, float, None] = Field(None, description="소개의원명", alias="INTD_ASBLM_NM")
    RCP_DT: Union[str, int, float, None] = Field(None, description="접수일자", alias="RCP_DT")
    JRCMIT_CMMT_DT: Union[str, int, float, None] = Field(None, description="소관위원회회부일", alias="JRCMIT_CMMT_DT")
    JRCMIT_NM: Union[str, int, float, None] = Field(None, description="소관위원회명", alias="JRCMIT_NM")
    RSLN_DT: Union[str, int, float, None] = Field(None, description="의결일자", alias="RSLN_DT")
    RSLN_RSLT: Union[str, int, float, None] = Field(None, description="의결결과", alias="RSLN_RSLT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11425(BaseModel):
    """Request parameters for OOWY4R001216HX11425"""
    NAAS_CD: str = Field(..., description="국회의원코드", alias="NAAS_CD")

class Model_OOWY4R001216HX11426(BaseModel):
    """Response model for OOWY4R001216HX11426"""
    PBLM_TTL: Union[str, int, float, None] = Field(None, description="발간물 제목", alias="PBLM_TTL")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="WRT_DT")
    DWLD_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="DWLD_URL")

class Params_OOWY4R001216HX11426(BaseModel):
    """Request parameters for OOWY4R001216HX11426"""
    PBLM_TTL: str | None = Field(None, description="발간물 제목", alias="PBLM_TTL")

class Model_OW1R4X0010744X17495(BaseModel):
    """Response model for OW1R4X0010744X17495"""
    AGE: Union[str, int, float, None] = Field(None, description="대수", alias="AGE")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NAME")
    BILL_KIND: Union[str, int, float, None] = Field(None, description="의안활동구분", alias="BILL_KIND")
    PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="의결결과", alias="PROC_RESULT_CD")
    VOTE_TCNT: Union[str, int, float, None] = Field(None, description="총투표수", alias="VOTE_TCNT")
    YES_TCNT: Union[str, int, float, None] = Field(None, description="찬성표수", alias="YES_TCNT")
    NO_TCNT: Union[str, int, float, None] = Field(None, description="반대수", alias="NO_TCNT")
    BLANK_TCNT: Union[str, int, float, None] = Field(None, description="기권수", alias="BLANK_TCNT")
    PROPOSE_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PROPOSE_DT")
    BDG_SUBMIT_DT: Union[str, int, float, None] = Field(None, description="예결위심사_회부일", alias="BDG_SUBMIT_DT")
    BDG_PRESENT_DT: Union[str, int, float, None] = Field(None, description="예결위심사_상정일", alias="BDG_PRESENT_DT")
    BDG_PROC_DT: Union[str, int, float, None] = Field(None, description="예결위심사_의결일", alias="BDG_PROC_DT")
    RGS_PRESENT_DT: Union[str, int, float, None] = Field(None, description="본회의심의_상정일", alias="RGS_PRESENT_DT")
    RGS_PROC_DT: Union[str, int, float, None] = Field(None, description="본회의심의_의결일", alias="RGS_PROC_DT")
    CURR_TRANS_DT: Union[str, int, float, None] = Field(None, description="정부이송일", alias="CURR_TRANS_DT")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위원회ID", alias="CURR_COMMITTEE_ID")
    COMMITTEE_NM: Union[str, int, float, None] = Field(None, description="소관위원회", alias="COMMITTEE_NM")

class Params_OW1R4X0010744X17495(BaseModel):
    """Request parameters for OW1R4X0010744X17495"""
    AGE: str = Field(..., description="대수", alias="AGE")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: str | None = Field(None, description="의안명", alias="BILL_NAME")
    BILL_KIND: str | None = Field(None, description="의안활동구분", alias="BILL_KIND")
    PROC_RESULT_CD: str | None = Field(None, description="의결결과", alias="PROC_RESULT_CD")
    PROPOSE_DT: str | None = Field(None, description="제안일", alias="PROPOSE_DT")
    RGS_PROC_DT: str | None = Field(None, description="본회의심의_의결일", alias="RGS_PROC_DT")
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")

class Model_O13FRZ001177X318752(BaseModel):
    """Response model for O13FRZ001177X318752"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_O13FRZ001177X318752(BaseModel):
    """Request parameters for O13FRZ001177X318752"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_O8XZ8U001160SW12010(BaseModel):
    """Response model for O8XZ8U001160SW12010"""
    ARTICLE_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="ARTICLE_TITLE")
    WRITER_NM: Union[str, int, float, None] = Field(None, description="작성자", alias="WRITER_NM")
    CATEGORY_ID: Union[str, int, float, None] = Field(None, description="분류번호", alias="CATEGORY_ID")
    CATEGORY_NM: Union[str, int, float, None] = Field(None, description="구분", alias="CATEGORY_NM")
    CREATE_DT: Union[str, int, float, None] = Field(None, description="등록일", alias="CREATE_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="상세보기URL", alias="LINK_URL")

class Params_O8XZ8U001160SW12010(BaseModel):
    """Request parameters for O8XZ8U001160SW12010"""
    ARTICLE_TITLE: str | None = Field(None, description="제목", alias="ARTICLE_TITLE")
    WRITER_NM: str | None = Field(None, description="작성자", alias="WRITER_NM")
    CREATE_DT: str | None = Field(None, description="등록일", alias="CREATE_DT")

class Model_OOWY4R001216HX11458(BaseModel):
    """Response model for OOWY4R001216HX11458"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_KIND: Union[str, int, float, None] = Field(None, description="의안 종류", alias="BILL_KIND")
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    PPSR_KIND: Union[str, int, float, None] = Field(None, description="제안자 구분", alias="PPSR_KIND")
    PPSL_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PPSL_DT")
    PROC_RSLT: Union[str, int, float, None] = Field(None, description="처리결과", alias="PROC_RSLT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11458(BaseModel):
    """Request parameters for OOWY4R001216HX11458"""
    ERACO: str | None = Field(None, description="대수", alias="ERACO")

class Model_OOWY4R001216HX11470(BaseModel):
    """Response model for OOWY4R001216HX11470"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    SESS_BG_DT: Union[str, int, float, None] = Field(None, description="회기시작일", alias="SESS_BG_DT")
    SESS_ED_DT: Union[str, int, float, None] = Field(None, description="회기종료일", alias="SESS_ED_DT")

class Params_OOWY4R001216HX11470(BaseModel):
    """Request parameters for OOWY4R001216HX11470"""
    pass

class Model_OSPS4X001105IL17344(BaseModel):
    """Response model for OSPS4X001105IL17344"""
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_OSPS4X001105IL17344(BaseModel):
    """Request parameters for OSPS4X001105IL17344"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: str | None = Field(None, description="등록일자", alias="INSERTDT")

class Model_OOBAOA001213RL17443(BaseModel):
    """Response model for OOBAOA001213RL17443"""
    INF_ID: Union[str, int, float, None] = Field(None, description="공공데이터ID", alias="INF_ID")
    INF_NM: Union[str, int, float, None] = Field(None, description="공공데이터명", alias="INF_NM")
    INF_EXP: Union[str, int, float, None] = Field(None, description="공공데이터설명", alias="INF_EXP")
    CATE_NM: Union[str, int, float, None] = Field(None, description="분류체계", alias="CATE_NM")
    OPEN_DTTM: Union[str, int, float, None] = Field(None, description="공개일자", alias="OPEN_DTTM")
    ORG_NM: Union[str, int, float, None] = Field(None, description="제공기관", alias="ORG_NM")
    LOAD_DTTM: Union[str, int, float, None] = Field(None, description="최종수정일자", alias="LOAD_DTTM")
    SRC_EXP: Union[str, int, float, None] = Field(None, description="원본시스템", alias="SRC_EXP")
    DDC_URL: Union[str, int, float, None] = Field(None, description="명세서URL", alias="DDC_URL")
    SRV_URL: Union[str, int, float, None] = Field(None, description="서비스URL", alias="SRV_URL")
    CCL_NM: Union[str, int, float, None] = Field(None, description="이용허락조건", alias="CCL_NM")
    LOAD_NM: Union[str, int, float, None] = Field(None, description="공개주기", alias="LOAD_NM")
    LOAD_CONT: Union[str, int, float, None] = Field(None, description="공개시기", alias="LOAD_CONT")

class Params_OOBAOA001213RL17443(BaseModel):
    """Request parameters for OOBAOA001213RL17443"""
    INF_ID: str | None = Field(None, description="공공데이터ID", alias="INF_ID")
    INF_NM: str | None = Field(None, description="공공데이터명", alias="INF_NM")
    SRC_EXP: str | None = Field(None, description="원본시스템", alias="SRC_EXP")

class Model_OOWY4R001216HX11421(BaseModel):
    """Response model for OOWY4R001216HX11421"""
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    UNCS_CNT: Union[str, int, float, None] = Field(None, description="위헌 개수", alias="UNCS_CNT")
    CLAW_MIS_CNT: Union[str, int, float, None] = Field(None, description="헌법 불일치 개수", alias="CLAW_MIS_CNT")
    OVER_CLAW_MIS_CNT: Union[str, int, float, None] = Field(None, description="헌법 불일치 개정시한 경과 개수", alias="OVER_CLAW_MIS_CNT")

class Params_OOWY4R001216HX11421(BaseModel):
    """Request parameters for OOWY4R001216HX11421"""
    pass

class Model_OVUY5B0009241I13320(BaseModel):
    """Response model for OVUY5B0009241I13320"""
    RPT_NO: Union[str, int, float, None] = Field(None, description="다운로드", alias="RPT_NO")
    RPT_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="RPT_TITLE")
    STND_DT: Union[str, int, float, None] = Field(None, description="기준일자", alias="STND_DT")
    WRT_NM: Union[str, int, float, None] = Field(None, description="작성자", alias="WRT_NM")
    UNIT_CD: Union[str, int, float, None] = Field(None, description="대별코드", alias="UNIT_CD")
    UNIT_NM: Union[str, int, float, None] = Field(None, description="대", alias="UNIT_NM")
    FILE_ID: Union[str, int, float, None] = Field(None, description="파일ID", alias="FILE_ID")

class Params_OVUY5B0009241I13320(BaseModel):
    """Request parameters for OVUY5B0009241I13320"""
    RPT_TITLE: str | None = Field(None, description="제목", alias="RPT_TITLE")
    STND_DT: str | None = Field(None, description="기준일자", alias="STND_DT")
    WRT_NM: str | None = Field(None, description="작성자", alias="WRT_NM")
    UNIT_NM: str | None = Field(None, description="대", alias="UNIT_NM")

class Model_OCAJQ4001000LI18751(BaseModel):
    """Response model for OCAJQ4001000LI18751"""
    DEPT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="DEPT_CD")
    DEPT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="DEPT_NM")
    JOB_RES_NM: Union[str, int, float, None] = Field(None, description="구성", alias="JOB_RES_NM")
    HG_NM: Union[str, int, float, None] = Field(None, description="위원명", alias="HG_NM")
    ORIG_NM: Union[str, int, float, None] = Field(None, description="선거구", alias="ORIG_NM")
    POLY_NM: Union[str, int, float, None] = Field(None, description="정당", alias="POLY_NM")
    ASSEM_TEL: Union[str, int, float, None] = Field(None, description="전화번호", alias="ASSEM_TEL")
    ASSEM_EMAIL: Union[str, int, float, None] = Field(None, description="이메일", alias="ASSEM_EMAIL")
    HJ_NM: Union[str, int, float, None] = Field(None, description="위원명(한자)", alias="HJ_NM")
    ROOM_NO: Union[str, int, float, None] = Field(None, description="호실", alias="ROOM_NO")
    STAFF: Union[str, int, float, None] = Field(None, description="보좌관", alias="STAFF")
    SECRETARY: Union[str, int, float, None] = Field(None, description="비서관", alias="SECRETARY")
    SECRETARY2: Union[str, int, float, None] = Field(None, description="비서", alias="SECRETARY2")
    MONA_CD: Union[str, int, float, None] = Field(None, description="국회의원코드", alias="MONA_CD")

class Params_OCAJQ4001000LI18751(BaseModel):
    """Request parameters for OCAJQ4001000LI18751"""
    DEPT_CD: str | None = Field(None, description="위원회코드", alias="DEPT_CD")
    DEPT_NM: str | None = Field(None, description="위원회명", alias="DEPT_NM")
    JOB_RES_NM: str | None = Field(None, description="구성", alias="JOB_RES_NM")
    HG_NM: str | None = Field(None, description="위원명", alias="HG_NM")
    ORIG_NM: str | None = Field(None, description="선거구", alias="ORIG_NM")
    POLY_NM: str | None = Field(None, description="정당", alias="POLY_NM")
    ASSEM_TEL: str | None = Field(None, description="전화번호", alias="ASSEM_TEL")
    ASSEM_EMAIL: str | None = Field(None, description="이메일", alias="ASSEM_EMAIL")
    MONA_CD: str | None = Field(None, description="국회의원코드", alias="MONA_CD")

class Model_OITFOE000968XH15981(BaseModel):
    """Response model for OITFOE000968XH15981"""
    EDU_TITLE_NM: Union[str, int, float, None] = Field(None, description="연수명", alias="EDU_TITLE_NM")
    EDU_OJR: Union[str, int, float, None] = Field(None, description="대상자", alias="EDU_OJR")
    EDU_PLC_NM: Union[str, int, float, None] = Field(None, description="장소", alias="EDU_PLC_NM")
    EDU_GUBUN_CD: Union[str, int, float, None] = Field(None, description="교육_대상자_구분코드", alias="EDU_GUBUN_CD")
    EDU_GUBUN_NM: Union[str, int, float, None] = Field(None, description="대상구분명", alias="EDU_GUBUN_NM")
    EDU_FXDNOPPL: Union[str, int, float, None] = Field(None, description="정원", alias="EDU_FXDNOPPL")
    CRT_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="CRT_DT")
    EDU_DPSTG_EXPENSE: Union[str, int, float, None] = Field(None, description="연수비", alias="EDU_DPSTG_EXPENSE")
    EDU_DT: Union[str, int, float, None] = Field(None, description="연수기간", alias="EDU_DT")
    EDU_APL_DT: Union[str, int, float, None] = Field(None, description="신청기간", alias="EDU_APL_DT")
    EDU_APL_CNC_DT: Union[str, int, float, None] = Field(None, description="취소가능기간", alias="EDU_APL_CNC_DT")

class Params_OITFOE000968XH15981(BaseModel):
    """Request parameters for OITFOE000968XH15981"""
    EDU_TITLE_NM: str | None = Field(None, description="연수명", alias="EDU_TITLE_NM")
    EDU_OJR: str | None = Field(None, description="대상자", alias="EDU_OJR")
    EDU_PLC_NM: str | None = Field(None, description="장소", alias="EDU_PLC_NM")
    EDU_GUBUN_NM: str | None = Field(None, description="대상구분명", alias="EDU_GUBUN_NM")
    EDU_DT: str | None = Field(None, description="연수기간", alias="EDU_DT")

class Model_O70WYZ000950T211169(BaseModel):
    """Response model for O70WYZ000950T211169"""
    ARTICLE_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="ARTICLE_TITLE")
    DT: Union[str, int, float, None] = Field(None, description="일시", alias="DT")
    ETC_CHAR11: Union[str, int, float, None] = Field(None, description="장소", alias="ETC_CHAR11")
    ARTICLE_TEXT: Union[str, int, float, None] = Field(None, description="내용", alias="ARTICLE_TEXT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크주소", alias="LINK_URL")

class Params_O70WYZ000950T211169(BaseModel):
    """Request parameters for O70WYZ000950T211169"""
    ARTICLE_TITLE: str | None = Field(None, description="제목", alias="ARTICLE_TITLE")
    DT: str | None = Field(None, description="일시", alias="DT")
    ETC_CHAR11: str | None = Field(None, description="장소", alias="ETC_CHAR11")

class Model_OOWY4R001216HX11433(BaseModel):
    """Response model for OOWY4R001216HX11433"""
    PBLM_TTL: Union[str, int, float, None] = Field(None, description="발간물 제목", alias="PBLM_TTL")
    WRT_DEPT: Union[str, int, float, None] = Field(None, description="작성부서", alias="WRT_DEPT")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11433(BaseModel):
    """Request parameters for OOWY4R001216HX11433"""
    PBLM_TTL: str | None = Field(None, description="발간물 제목", alias="PBLM_TTL")

class Model_OPP4KM0012097716578(BaseModel):
    """Response model for OPP4KM0012097716578"""
    TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="TITLE")
    CHIEF_RESRCH: Union[str, int, float, None] = Field(None, description="연구 책임자", alias="CHIEF_RESRCH")
    REG_DTTM: Union[str, int, float, None] = Field(None, description="작성일", alias="REG_DTTM")
    DETAIL_URL: Union[str, int, float, None] = Field(None, description="상세 URL", alias="DETAIL_URL")

class Params_OPP4KM0012097716578(BaseModel):
    """Request parameters for OPP4KM0012097716578"""
    pass

class Model_OFUAJ6001108BJ11284(BaseModel):
    """Response model for OFUAJ6001108BJ11284"""
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_OFUAJ6001108BJ11284(BaseModel):
    """Request parameters for OFUAJ6001108BJ11284"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: str | None = Field(None, description="등록일자", alias="INSERTDT")

class Model_OOWY4R001216HX11517(BaseModel):
    """Response model for OOWY4R001216HX11517"""
    CONF_KND: Union[str, int, float, None] = Field(None, description="회의종류", alias="CONF_KND")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    FILE_KND: Union[str, int, float, None] = Field(None, description="파일종류", alias="FILE_KND")
    FILE_CN: Union[str, int, float, None] = Field(None, description="파일설명", alias="FILE_CN")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11517(BaseModel):
    """Request parameters for OOWY4R001216HX11517"""
    ERACO: str | None = Field(None, description="대수", alias="ERACO")
    CONF_ID: str | None = Field(None, description="회의ID", alias="CONF_ID")

class Model_OEUJQB0012145514537(BaseModel):
    """Response model for OEUJQB0012145514537"""
    UNIT_CD: Union[str, int, float, None] = Field(None, description="대수", alias="UNIT_CD")
    UNIT_NM: Union[str, int, float, None] = Field(None, description="대수", alias="UNIT_NM")
    MEETINGSESSION: Union[str, int, float, None] = Field(None, description="회기", alias="MEETINGSESSION")
    CHA: Union[str, int, float, None] = Field(None, description="차수", alias="CHA")
    TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="TITLE")
    MEETTING_DATE: Union[str, int, float, None] = Field(None, description="일자", alias="MEETTING_DATE")
    MEETTING_TIME: Union[str, int, float, None] = Field(None, description="일시", alias="MEETTING_TIME")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크주소", alias="LINK_URL")

class Params_OEUJQB0012145514537(BaseModel):
    """Request parameters for OEUJQB0012145514537"""
    UNIT_CD: str = Field(..., description="대수", alias="UNIT_CD")
    MEETINGSESSION: str | None = Field(None, description="회기", alias="MEETINGSESSION")
    CHA: str | None = Field(None, description="차수", alias="CHA")
    TITLE: str | None = Field(None, description="제목", alias="TITLE")
    MEETTING_DATE: str | None = Field(None, description="일자", alias="MEETTING_DATE")

class Model_ORMXPX0011135N18074(BaseModel):
    """Response model for ORMXPX0011135N18074"""
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_ORMXPX0011135N18074(BaseModel):
    """Request parameters for ORMXPX0011135N18074"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: str | None = Field(None, description="등록일자", alias="INSERTDT")

class Model_O8685D0008489413266(BaseModel):
    """Response model for O8685D0008489413266"""
    RPT_NO: Union[str, int, float, None] = Field(None, description="다운로드", alias="RPT_NO")
    YEAR: Union[str, int, float, None] = Field(None, description="년도", alias="YEAR")
    FILE_ID: Union[str, int, float, None] = Field(None, description="파일ID", alias="FILE_ID")
    RPT_TITLE: Union[str, int, float, None] = Field(None, description="보고서제목", alias="RPT_TITLE")
    RG_DE: Union[str, int, float, None] = Field(None, description="등록일", alias="RG_DE")
    UNIT_CD: Union[str, int, float, None] = Field(None, description="대별코드", alias="UNIT_CD")
    UNIT_NM: Union[str, int, float, None] = Field(None, description="대", alias="UNIT_NM")
    ASBLM_NM: Union[str, int, float, None] = Field(None, description="의원명", alias="ASBLM_NM")
    QUARTER: Union[str, int, float, None] = Field(None, description="분기", alias="QUARTER")
    DIV_NM: Union[str, int, float, None] = Field(None, description="구분명", alias="DIV_NM")

class Params_O8685D0008489413266(BaseModel):
    """Request parameters for O8685D0008489413266"""
    YEAR: str | None = Field(None, description="년도", alias="YEAR")
    ASBLM_NM: str | None = Field(None, description="의원명", alias="ASBLM_NM")
    UNIT_NM: str | None = Field(None, description="대", alias="UNIT_NM")
    RPT_TITLE: str | None = Field(None, description="보고서제목", alias="RPT_TITLE")
    UNIT_CD: str = Field(..., description="대별코드", alias="UNIT_CD")
    QUARTER: str | None = Field(None, description="분기", alias="QUARTER")
    DIV_NM: str | None = Field(None, description="구분명", alias="DIV_NM")

class Model_OKBFLN000963SS13091(BaseModel):
    """Response model for OKBFLN000963SS13091"""
    MEETING_DATE: Union[str, int, float, None] = Field(None, description="회의일자", alias="MEETING_DATE")
    MEETING_TIME: Union[str, int, float, None] = Field(None, description="시간", alias="MEETING_TIME")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DEGREE: Union[str, int, float, None] = Field(None, description="차수", alias="DEGREE")
    TITLE: Union[str, int, float, None] = Field(None, description="구분", alias="TITLE")
    COMMITTEE_NAME: Union[str, int, float, None] = Field(None, description="위원회 명", alias="COMMITTEE_NAME")
    LINK_URL2: Union[str, int, float, None] = Field(None, description="상세_URL", alias="LINK_URL2")
    UNIT_CD: Union[str, int, float, None] = Field(None, description="대수", alias="UNIT_CD")
    UNIT_NM: Union[str, int, float, None] = Field(None, description="대수", alias="UNIT_NM")
    HR_DEPT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="HR_DEPT_CD")
    ANGUN: Union[str, int, float, None] = Field(None, description="안건", alias="ANGUN")

class Params_OKBFLN000963SS13091(BaseModel):
    """Request parameters for OKBFLN000963SS13091"""
    MEETING_DATE: str | None = Field(None, description="회의일자", alias="MEETING_DATE")
    MEETING_TIME: str | None = Field(None, description="시간", alias="MEETING_TIME")
    SESS: str | None = Field(None, description="회기", alias="SESS")
    DEGREE: str | None = Field(None, description="차수", alias="DEGREE")
    TITLE: str | None = Field(None, description="구분", alias="TITLE")
    COMMITTEE_NAME: str | None = Field(None, description="위원회 명", alias="COMMITTEE_NAME")
    UNIT_CD: str = Field(..., description="대수", alias="UNIT_CD")
    HR_DEPT_CD: str | None = Field(None, description="위원회코드", alias="HR_DEPT_CD")

class Model_O6MC3G0011698G17444(BaseModel):
    """Response model for O6MC3G0011698G17444"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_O6MC3G0011698G17444(BaseModel):
    """Request parameters for O6MC3G0011698G17444"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_ORMEIR001164VQ17801(BaseModel):
    """Response model for ORMEIR001164VQ17801"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_ORMEIR001164VQ17801(BaseModel):
    """Request parameters for ORMEIR001164VQ17801"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_OFOEZN001060N312362(BaseModel):
    """Response model for OFOEZN001060N312362"""
    COMP_MAIN_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="COMP_MAIN_TITLE")
    REG_DATE: Union[str, int, float, None] = Field(None, description="등록일자", alias="REG_DATE")
    COMP_CONTENT: Union[str, int, float, None] = Field(None, description="내용", alias="COMP_CONTENT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="상세보기", alias="LINK_URL")

class Params_OFOEZN001060N312362(BaseModel):
    """Request parameters for OFOEZN001060N312362"""
    COMP_MAIN_TITLE: str | None = Field(None, description="제목", alias="COMP_MAIN_TITLE")
    COMP_CONTENT: str | None = Field(None, description="내용", alias="COMP_CONTENT")

class Model_OOWY4R001216HX11508(BaseModel):
    """Response model for OOWY4R001216HX11508"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    CONF_KND: Union[str, int, float, None] = Field(None, description="회의종류", alias="CONF_KND")
    CMIT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="CMIT_CD")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운로드 URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11508(BaseModel):
    """Request parameters for OOWY4R001216HX11508"""
    ERACO: str = Field(..., description="대수", alias="ERACO")
    CMIT_CD: str | None = Field(None, description="위원회코드", alias="CMIT_CD")

class Model_OOWY4R001216HX11446(BaseModel):
    """Response model for OOWY4R001216HX11446"""
    MTR_DIV: Union[str, int, float, None] = Field(None, description="발간자료구분", alias="MTR_DIV")
    MTR_TTL: Union[str, int, float, None] = Field(None, description="발간자료제목", alias="MTR_TTL")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 URL", alias="LINK_URL")

class Params_OOWY4R001216HX11446(BaseModel):
    """Request parameters for OOWY4R001216HX11446"""
    MTR_DIV: str | None = Field(None, description="발간자료구분", alias="MTR_DIV")
    MTR_TTL: str | None = Field(None, description="발간자료제목", alias="MTR_TTL")

class Model_OOWY4R001216HX11415(BaseModel):
    """Response model for OOWY4R001216HX11415"""
    SCH_KIND: Union[str, int, float, None] = Field(None, description="일정종류", alias="SCH_KIND")
    SCH_CN: Union[str, int, float, None] = Field(None, description="일정내용", alias="SCH_CN")
    SCH_DT: Union[str, int, float, None] = Field(None, description="일자", alias="SCH_DT")
    SCH_TM: Union[str, int, float, None] = Field(None, description="시간", alias="SCH_TM")
    CONF_DIV: Union[str, int, float, None] = Field(None, description="회의구분", alias="CONF_DIV")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    CONF_SESS: Union[str, int, float, None] = Field(None, description="회의회기", alias="CONF_SESS")
    CONF_DGR: Union[str, int, float, None] = Field(None, description="회의차수", alias="CONF_DGR")

class Params_OOWY4R001216HX11415(BaseModel):
    """Request parameters for OOWY4R001216HX11415"""
    NAAS_CD: str = Field(..., description="국회의원코드", alias="NAAS_CD")

class Model_OQ0WH1000975M912523(BaseModel):
    """Response model for OQ0WH1000975M912523"""
    V_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="V_TITLE")
    URL_LINK: Union[str, int, float, None] = Field(None, description="기사 URL", alias="URL_LINK")
    DATE_LASTMODIFIED: Union[str, int, float, None] = Field(None, description="최종수정일", alias="DATE_LASTMODIFIED")
    DATE_RELEASED: Union[str, int, float, None] = Field(None, description="기사작성일", alias="DATE_RELEASED")
    V_BODY: Union[str, int, float, None] = Field(None, description="기사내용", alias="V_BODY")

class Params_OQ0WH1000975M912523(BaseModel):
    """Request parameters for OQ0WH1000975M912523"""
    V_TITLE: str | None = Field(None, description="제목", alias="V_TITLE")

class Model_OOWY4R001216HX11451(BaseModel):
    """Response model for OOWY4R001216HX11451"""
    CONF_SCH_DIV: Union[str, int, float, None] = Field(None, description="회의일정 구분", alias="CONF_SCH_DIV")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    SCH_DT: Union[str, int, float, None] = Field(None, description="일자", alias="SCH_DT")
    SCH_TM: Union[str, int, float, None] = Field(None, description="시간", alias="SCH_TM")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")

class Params_OOWY4R001216HX11451(BaseModel):
    """Request parameters for OOWY4R001216HX11451"""
    CONF_SCH_DIV: str | None = Field(None, description="회의일정 구분", alias="CONF_SCH_DIV")
    SCH_DT: str | None = Field(None, description="일자", alias="SCH_DT")

class Model_OOWY4R001216HX11422(BaseModel):
    """Response model for OOWY4R001216HX11422"""
    REV_LAW_SITU_TTLL: Union[str, int, float, None] = Field(None, description="개정대상법률현황제목", alias="REV_LAW_SITU_TTLL")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일자", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 URL", alias="LINK_URL")

class Params_OOWY4R001216HX11422(BaseModel):
    """Request parameters for OOWY4R001216HX11422"""
    REV_LAW_SITU_TTLL: str | None = Field(None, description="개정대상법률현황제목", alias="REV_LAW_SITU_TTLL")

class Model_OY18U4001075AG16626(BaseModel):
    """Response model for OY18U4001075AG16626"""
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="의안명(한글)", alias="BILL_NAME")
    PROPOSER: Union[str, int, float, None] = Field(None, description="제안자", alias="PROPOSER")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위", alias="CURR_COMMITTEE")
    PROPOSE_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PROPOSE_DT")
    URL: Union[str, int, float, None] = Field(None, description="링크주소", alias="URL")
    LAW_PRESENT_DT: Union[str, int, float, None] = Field(None, description="법사위상정일", alias="LAW_PRESENT_DT")
    LAW_PROC_DT: Union[str, int, float, None] = Field(None, description="법사위처리일", alias="LAW_PROC_DT")
    LAW_PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="법사위처리결과", alias="LAW_PROC_RESULT_CD")
    RST_PROPOSER: Union[str, int, float, None] = Field(None, description="대표발의자", alias="RST_PROPOSER")
    LAW_SUBMIT_DT: Union[str, int, float, None] = Field(None, description="법사위회부일", alias="LAW_SUBMIT_DT")
    CMT_PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="소관위처리결과", alias="CMT_PROC_RESULT_CD")
    CMT_PROC_DT: Union[str, int, float, None] = Field(None, description="소관위처리일", alias="CMT_PROC_DT")
    CMT_PRESENT_DT: Union[str, int, float, None] = Field(None, description="소관위상정일", alias="CMT_PRESENT_DT")
    RST_MONA_CD: Union[str, int, float, None] = Field(None, description="대표발의자코드", alias="RST_MONA_CD")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    AGE: Union[str, int, float, None] = Field(None, description="대(현)", alias="AGE")
    COMMITTEE_DT: Union[str, int, float, None] = Field(None, description="소관위회부일", alias="COMMITTEE_DT")

class Params_OY18U4001075AG16626(BaseModel):
    """Request parameters for OY18U4001075AG16626"""
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: str | None = Field(None, description="의안명(한글)", alias="BILL_NAME")
    PROPOSER: str | None = Field(None, description="제안자", alias="PROPOSER")
    CURR_COMMITTEE: str = Field(..., description="소관위", alias="CURR_COMMITTEE")
    PROPOSE_DT: str | None = Field(None, description="제안일", alias="PROPOSE_DT")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")

class Model_OOWY4R001216HX11424(BaseModel):
    """Response model for OOWY4R001216HX11424"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    CONF_PTM: Union[str, int, float, None] = Field(None, description="회의시간", alias="CONF_PTM")
    CONF_NM: Union[str, int, float, None] = Field(None, description="회의명", alias="CONF_NM")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11424(BaseModel):
    """Request parameters for OOWY4R001216HX11424"""
    ERACO: str | None = Field(None, description="대수", alias="ERACO")
    CONF_DT: str | None = Field(None, description="회의일자", alias="CONF_DT")

class Model_OOWY4R001216HX11525(BaseModel):
    """Response model for OOWY4R001216HX11525"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안 ID", alias="BILL_ID")
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 URL", alias="LINK_URL")

class Params_OOWY4R001216HX11525(BaseModel):
    """Request parameters for OOWY4R001216HX11525"""
    CONF_ID: str | None = Field(None, description="회의ID", alias="CONF_ID")
    BILL_ID: str | None = Field(None, description="의안 ID", alias="BILL_ID")

class Model_OET0D9001078G318850(BaseModel):
    """Response model for OET0D9001078G318850"""
    HG_NM: Union[str, int, float, None] = Field(None, description="이름", alias="HG_NM")
    T_URL: Union[str, int, float, None] = Field(None, description="트위터 URL", alias="T_URL")
    F_URL: Union[str, int, float, None] = Field(None, description="페이스북 URL", alias="F_URL")
    Y_URL: Union[str, int, float, None] = Field(None, description="유튜브 URL", alias="Y_URL")
    B_URL: Union[str, int, float, None] = Field(None, description="블로그 URL", alias="B_URL")
    MONA_CD: Union[str, int, float, None] = Field(None, description="국회의원코드", alias="MONA_CD")

class Params_OET0D9001078G318850(BaseModel):
    """Request parameters for OET0D9001078G318850"""
    HG_NM: str | None = Field(None, description="이름", alias="HG_NM")
    MONA_CD: str | None = Field(None, description="국회의원코드", alias="MONA_CD")

class Model_OOWY4R001216HX11520(BaseModel):
    """Response model for OOWY4R001216HX11520"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    CONF_KND: Union[str, int, float, None] = Field(None, description="회의종류", alias="CONF_KND")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    SB_CMIT_NM: Union[str, int, float, None] = Field(None, description="소위원회명", alias="SB_CMIT_NM")
    CONF_PLC: Union[str, int, float, None] = Field(None, description="회의장소", alias="CONF_PLC")
    BG_PTM: Union[str, int, float, None] = Field(None, description="시작시간", alias="BG_PTM")
    ED_PTM: Union[str, int, float, None] = Field(None, description="종료시간", alias="ED_PTM")
    CONF_PTM: Union[str, int, float, None] = Field(None, description="회의시간", alias="CONF_PTM")
    HR_HRG_YN: Union[str, int, float, None] = Field(None, description="인사청문회여부", alias="HR_HRG_YN")
    PBHRG_YN: Union[str, int, float, None] = Field(None, description="공청회여부", alias="PBHRG_YN")
    HRG_YN: Union[str, int, float, None] = Field(None, description="청문회여부", alias="HRG_YN")
    SITG_YN: Union[str, int, float, None] = Field(None, description="연석회의여부", alias="SITG_YN")
    RMND_SPH_YN: Union[str, int, float, None] = Field(None, description="대통령위임연설여부", alias="RMND_SPH_YN")
    RDJM_SPH_YN: Union[str, int, float, None] = Field(None, description="대통령시정연설여부", alias="RDJM_SPH_YN")
    FRNGUS_SPH_YN: Union[str, int, float, None] = Field(None, description="외빈연설여부", alias="FRNGUS_SPH_YN")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운로드 URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11520(BaseModel):
    """Request parameters for OOWY4R001216HX11520"""
    CONF_ID: str = Field(..., description="회의ID", alias="CONF_ID")

class Model_OLI05G0011283N16926(BaseModel):
    """Response model for OLI05G0011283N16926"""
    PRDC_YM_NM: Union[str, int, float, None] = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: Union[str, int, float, None] = Field(None, description="공개파일명", alias="OPB_FL_NM")
    INST_CD: Union[str, int, float, None] = Field(None, description="기관코드", alias="INST_CD")
    INST_NM: Union[str, int, float, None] = Field(None, description="기관명", alias="INST_NM")
    OPB_FL_PH: Union[str, int, float, None] = Field(None, description="공개파일경로", alias="OPB_FL_PH")
    FILE_ID: Union[str, int, float, None] = Field(None, description="파일ID", alias="FILE_ID")

class Params_OLI05G0011283N16926(BaseModel):
    """Request parameters for OLI05G0011283N16926"""
    PRDC_YM: str | None = Field(None, description="생산년월", alias="PRDC_YM")
    OPB_FL_NM: str | None = Field(None, description="공개파일명", alias="OPB_FL_NM")

class Model_OOWY4R001216HX11417(BaseModel):
    """Response model for OOWY4R001216HX11417"""
    SCH_KIND: Union[str, int, float, None] = Field(None, description="일정종류", alias="SCH_KIND")
    SCH_CN: Union[str, int, float, None] = Field(None, description="일정내용", alias="SCH_CN")
    SCH_DT: Union[str, int, float, None] = Field(None, description="일자", alias="SCH_DT")
    SCH_TM: Union[str, int, float, None] = Field(None, description="시간", alias="SCH_TM")
    CONF_DIV: Union[str, int, float, None] = Field(None, description="회의구분", alias="CONF_DIV")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    CONF_SESS: Union[str, int, float, None] = Field(None, description="회의회기", alias="CONF_SESS")
    CONF_DGR: Union[str, int, float, None] = Field(None, description="회의차수", alias="CONF_DGR")

class Params_OOWY4R001216HX11417(BaseModel):
    """Request parameters for OOWY4R001216HX11417"""
    NAAS_CD: str = Field(..., description="국회의원코드", alias="NAAS_CD")

class Model_OOWY4R001216HX11501(BaseModel):
    """Response model for OOWY4R001216HX11501"""
    NAAS_NM: Union[str, int, float, None] = Field(None, description="국회의원명", alias="NAAS_NM")
    EV_TTL: Union[str, int, float, None] = Field(None, description="행사 제목", alias="EV_TTL")
    EV_DTM: Union[str, int, float, None] = Field(None, description="행사 일시", alias="EV_DTM")
    EV_PLC: Union[str, int, float, None] = Field(None, description="행사 장소", alias="EV_PLC")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11501(BaseModel):
    """Request parameters for OOWY4R001216HX11501"""
    pass

class Model_O6KN2D001106O610167(BaseModel):
    """Response model for O6KN2D001106O610167"""
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_O6KN2D001106O610167(BaseModel):
    """Request parameters for O6KN2D001106O610167"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: str | None = Field(None, description="등록일자", alias="INSERTDT")

class Model_OH01G5001175B914429(BaseModel):
    """Response model for OH01G5001175B914429"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_OH01G5001175B914429(BaseModel):
    """Request parameters for OH01G5001175B914429"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_OTA0YC001127RJ11880(BaseModel):
    """Response model for OTA0YC001127RJ11880"""
    PRDC_YM_NM: Union[str, int, float, None] = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: Union[str, int, float, None] = Field(None, description="공개파일명", alias="OPB_FL_NM")
    INST_CD: Union[str, int, float, None] = Field(None, description="기관코드", alias="INST_CD")
    INST_NM: Union[str, int, float, None] = Field(None, description="기관명", alias="INST_NM")
    OPB_FL_PH: Union[str, int, float, None] = Field(None, description="공개파일경로", alias="OPB_FL_PH")
    FILE_ID: Union[str, int, float, None] = Field(None, description="파일ID", alias="FILE_ID")

class Params_OTA0YC001127RJ11880(BaseModel):
    """Request parameters for OTA0YC001127RJ11880"""
    PRDC_YM: str | None = Field(None, description="생산년월", alias="PRDC_YM")
    OPB_FL_NM: str | None = Field(None, description="공개파일명", alias="OPB_FL_NM")

class Model_OOWY4R001216HX11513(BaseModel):
    """Response model for OOWY4R001216HX11513"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    CONF_KND: Union[str, int, float, None] = Field(None, description="회의종류", alias="CONF_KND")
    CMIT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="CMIT_CD")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운로드 URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11513(BaseModel):
    """Request parameters for OOWY4R001216HX11513"""
    ERACO: str = Field(..., description="대수", alias="ERACO")
    CMIT_CD: str | None = Field(None, description="위원회코드", alias="CMIT_CD")

class Model_ODFFIG001072OX10139(BaseModel):
    """Response model for ODFFIG001072OX10139"""
    AGE: Union[str, int, float, None] = Field(None, description="대수", alias="AGE")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    BILL_KIND: Union[str, int, float, None] = Field(None, description="의안활동구분", alias="BILL_KIND")
    PROPOSER_KIND_CD: Union[str, int, float, None] = Field(None, description="제안자구분", alias="PROPOSER_KIND_CD")
    PROPOSER: Union[str, int, float, None] = Field(None, description="제안자", alias="PROPOSER")
    COMMITTEE_NM: Union[str, int, float, None] = Field(None, description="소관위원회", alias="COMMITTEE_NM")
    PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="의결결과", alias="PROC_RESULT_CD")
    VOTE_TCNT: Union[str, int, float, None] = Field(None, description="총투표수", alias="VOTE_TCNT")
    YES_TCNT: Union[str, int, float, None] = Field(None, description="찬성", alias="YES_TCNT")
    NO_TCNT: Union[str, int, float, None] = Field(None, description="반대", alias="NO_TCNT")
    BLANK_TCNT: Union[str, int, float, None] = Field(None, description="기권", alias="BLANK_TCNT")
    PROPOSE_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PROPOSE_DT")
    COMMITTEE_SUBMIT_DT: Union[str, int, float, None] = Field(None, description="위원회심사_회부일", alias="COMMITTEE_SUBMIT_DT")
    COMMITTEE_PRESENT_DT: Union[str, int, float, None] = Field(None, description="위원회심사_상정일", alias="COMMITTEE_PRESENT_DT")
    COMMITTEE_PROC_DT: Union[str, int, float, None] = Field(None, description="위원회심사_의결일", alias="COMMITTEE_PROC_DT")
    RGS_PRESENT_DT: Union[str, int, float, None] = Field(None, description="본회의심의_상정일", alias="RGS_PRESENT_DT")
    RGS_PROC_DT: Union[str, int, float, None] = Field(None, description="본회의심의_의결일", alias="RGS_PROC_DT")
    CURR_TRANS_DT: Union[str, int, float, None] = Field(None, description="정부이송일", alias="CURR_TRANS_DT")
    ANNOUNCE_DT: Union[str, int, float, None] = Field(None, description="공포일", alias="ANNOUNCE_DT")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위원회ID", alias="CURR_COMMITTEE_ID")

class Params_ODFFIG001072OX10139(BaseModel):
    """Request parameters for ODFFIG001072OX10139"""
    AGE: str = Field(..., description="대수", alias="AGE")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NM: str | None = Field(None, description="의안명", alias="BILL_NM")
    PROPOSER_KIND_CD: str | None = Field(None, description="제안자구분", alias="PROPOSER_KIND_CD")
    PROPOSER: str | None = Field(None, description="제안자", alias="PROPOSER")
    COMMITTEE_NM: str | None = Field(None, description="소관위원회", alias="COMMITTEE_NM")
    PROC_RESULT_CD: str | None = Field(None, description="의결결과", alias="PROC_RESULT_CD")
    PROPOSE_DT: str | None = Field(None, description="제안일", alias="PROPOSE_DT")
    RGS_PROC_DT: str | None = Field(None, description="본회의심의_의결일", alias="RGS_PROC_DT")
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위원회ID", alias="CURR_COMMITTEE_ID")

class Model_OOWY4R001216HX11431(BaseModel):
    """Response model for OOWY4R001216HX11431"""
    SCH_DT: Union[str, int, float, None] = Field(None, description="일자", alias="SCH_DT")
    SCH_TM: Union[str, int, float, None] = Field(None, description="시간", alias="SCH_TM")
    CHM_DIV: Union[str, int, float, None] = Field(None, description="의장단구분(의장, 부의장 구분)", alias="CHM_DIV")
    SCH_CN: Union[str, int, float, None] = Field(None, description="일정내용", alias="SCH_CN")

class Params_OOWY4R001216HX11431(BaseModel):
    """Request parameters for OOWY4R001216HX11431"""
    SCH_DT: str | None = Field(None, description="일자", alias="SCH_DT")
    CHM_DIV: str | None = Field(None, description="의장단구분(의장, 부의장 구분)", alias="CHM_DIV")

class Model_OQG5IZ0011449610187(BaseModel):
    """Response model for OQG5IZ0011449610187"""
    DAESU: Union[str, int, float, None] = Field(None, description="대수", alias="DAESU")
    DAE: Union[str, int, float, None] = Field(None, description="대별 및 소속정당(단체)", alias="DAE")
    DAE_NM: Union[str, int, float, None] = Field(None, description="대별", alias="DAE_NM")
    NAME: Union[str, int, float, None] = Field(None, description="이름", alias="NAME")
    NAME_HAN: Union[str, int, float, None] = Field(None, description="이름(한자)", alias="NAME_HAN")
    JA: Union[str, int, float, None] = Field(None, description="자", alias="JA")
    HO: Union[str, int, float, None] = Field(None, description="호", alias="HO")
    BIRTH: Union[str, int, float, None] = Field(None, description="생년월일", alias="BIRTH")
    BON: Union[str, int, float, None] = Field(None, description="본관", alias="BON")
    POSI: Union[str, int, float, None] = Field(None, description="출생지", alias="POSI")
    HAK: Union[str, int, float, None] = Field(None, description="학력 및 경력", alias="HAK")
    HOBBY: Union[str, int, float, None] = Field(None, description="종교 및 취미", alias="HOBBY")
    BOOK: Union[str, int, float, None] = Field(None, description="저서", alias="BOOK")
    SANG: Union[str, int, float, None] = Field(None, description="상훈", alias="SANG")
    DEAD: Union[str, int, float, None] = Field(None, description="기타정보(사망일)", alias="DEAD")
    URL: Union[str, int, float, None] = Field(None, description="회원정보 확인 헌정회 홈페이지 URL", alias="URL")

class Params_OQG5IZ0011449610187(BaseModel):
    """Request parameters for OQG5IZ0011449610187"""
    DAESU: str = Field(..., description="대수", alias="DAESU")
    DAE: str | None = Field(None, description="대별 및 소속정당(단체)", alias="DAE")
    DAE_NM: str | None = Field(None, description="대별", alias="DAE_NM")
    NAME: str | None = Field(None, description="이름", alias="NAME")
    BIRTH: str | None = Field(None, description="생년월일", alias="BIRTH")
    BON: str | None = Field(None, description="본관", alias="BON")
    POSI: str | None = Field(None, description="출생지", alias="POSI")

class Model_O0TLLI0008796R14875(BaseModel):
    """Response model for O0TLLI0008796R14875"""
    YR: Union[str, int, float, None] = Field(None, description="연도", alias="YR")
    PN: Union[str, int, float, None] = Field(None, description="성명", alias="PN")
    RTR_DT: Union[str, int, float, None] = Field(None, description="퇴직일", alias="RTR_DT")
    RTR_THEN_PSIT_NM: Union[str, int, float, None] = Field(None, description="퇴직 시 직위", alias="RTR_THEN_PSIT_NM")
    GETJOB_INST_NM: Union[str, int, float, None] = Field(None, description="취업기관", alias="GETJOB_INST_NM")
    GETJOB_DT: Union[str, int, float, None] = Field(None, description="취업일", alias="GETJOB_DT")
    PSIT_NM: Union[str, int, float, None] = Field(None, description="직위", alias="PSIT_NM")

class Params_O0TLLI0008796R14875(BaseModel):
    """Request parameters for O0TLLI0008796R14875"""
    YR: str | None = Field(None, description="연도", alias="YR")
    PN: str | None = Field(None, description="성명", alias="PN")
    RTR_THEN_PSIT_NM: str | None = Field(None, description="퇴직 시 직위", alias="RTR_THEN_PSIT_NM")
    GETJOB_INST_NM: str | None = Field(None, description="취업기관", alias="GETJOB_INST_NM")
    PSIT_NM: str | None = Field(None, description="직위", alias="PSIT_NM")

class Model_OOWY4R001216HX11514(BaseModel):
    """Response model for OOWY4R001216HX11514"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    CONF_KND: Union[str, int, float, None] = Field(None, description="회의종류", alias="CONF_KND")
    CMIT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="CMIT_CD")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운로드 URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11514(BaseModel):
    """Request parameters for OOWY4R001216HX11514"""
    ERACO: str = Field(..., description="대수", alias="ERACO")
    CMIT_CD: str | None = Field(None, description="위원회코드", alias="CMIT_CD")

class Model_OOWY4R001216HX11420(BaseModel):
    """Response model for OOWY4R001216HX11420"""
    BRDI_TTL: Union[str, int, float, None] = Field(None, description="게시물 제목", alias="BRDI_TTL")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 URL", alias="LINK_URL")

class Params_OOWY4R001216HX11420(BaseModel):
    """Request parameters for OOWY4R001216HX11420"""
    BRDI_TTL: str | None = Field(None, description="게시물 제목", alias="BRDI_TTL")

class Model_O1O34T000932VG10613(BaseModel):
    """Response model for O1O34T000932VG10613"""
    FSCL_YY: Union[str, int, float, None] = Field(None, description="회계년도", alias="FSCL_YY")
    EXE_M: Union[str, int, float, None] = Field(None, description="집행월", alias="EXE_M")
    FSCL_NM: Union[str, int, float, None] = Field(None, description="회계명", alias="FSCL_NM")
    FLD_NM: Union[str, int, float, None] = Field(None, description="분야명", alias="FLD_NM")
    SECT_NM: Union[str, int, float, None] = Field(None, description="부문명", alias="SECT_NM")
    PGM_NM: Union[str, int, float, None] = Field(None, description="프로그램명", alias="PGM_NM")
    ACTV_NM: Union[str, int, float, None] = Field(None, description="단위사업명", alias="ACTV_NM")
    ANEXP_BDG_CAMT: Union[str, int, float, None] = Field(None, description="예산", alias="ANEXP_BDG_CAMT")
    EP_AMT: Union[str, int, float, None] = Field(None, description="당월집행액", alias="EP_AMT")
    THISM_AGGR_EP_AMT: Union[str, int, float, None] = Field(None, description="누계집행액", alias="THISM_AGGR_EP_AMT")

class Params_O1O34T000932VG10613(BaseModel):
    """Request parameters for O1O34T000932VG10613"""
    FSCL_YY: str | None = Field(None, description="회계년도", alias="FSCL_YY")
    EXE_M: str | None = Field(None, description="집행월", alias="EXE_M")
    FSCL_NM: str | None = Field(None, description="회계명", alias="FSCL_NM")
    FLD_NM: str | None = Field(None, description="분야명", alias="FLD_NM")
    SECT_NM: str | None = Field(None, description="부문명", alias="SECT_NM")
    PGM_NM: str | None = Field(None, description="프로그램명", alias="PGM_NM")
    ACTV_NM: str | None = Field(None, description="단위사업명", alias="ACTV_NM")

class Model_ON9NSL000857D116126(BaseModel):
    """Response model for ON9NSL000857D116126"""
    DIV: Union[str, int, float, None] = Field(None, description="구분", alias="DIV")
    POL_RSC_RPT: Union[str, int, float, None] = Field(None, description="정책연구보고서", alias="POL_RSC_RPT")
    LEG_INIT: Union[str, int, float, None] = Field(None, description="법안제개정 등 발의", alias="LEG_INIT")
    SEMINAR: Union[str, int, float, None] = Field(None, description="세미나 공청회등(전시회 포함)", alias="SEMINAR")
    CONF: Union[str, int, float, None] = Field(None, description="간담회 등(언론보도 포함)", alias="CONF")
    RESC: Union[str, int, float, None] = Field(None, description="각종조사활동 등", alias="RESC")
    DIV2: Union[str, int, float, None] = Field(None, description="연도", alias="DIV2")

class Params_ON9NSL000857D116126(BaseModel):
    """Request parameters for ON9NSL000857D116126"""
    DIV: str | None = Field(None, description="구분", alias="DIV")
    POL_RSC_RPT: str | None = Field(None, description="정책연구보고서", alias="POL_RSC_RPT")
    DIV2: str | None = Field(None, description="연도", alias="DIV2")

class Model_OD21030011944P19666(BaseModel):
    """Response model for OD21030011944P19666"""
    HG_NM: Union[str, int, float, None] = Field(None, description="의원이름(한글)", alias="HG_NM")
    HJ_NM: Union[str, int, float, None] = Field(None, description="의원이름(한자)", alias="HJ_NM")
    FRTO_DATE: Union[str, int, float, None] = Field(None, description="활동기간", alias="FRTO_DATE")
    PROFILE_SJ: Union[str, int, float, None] = Field(None, description="의원이력", alias="PROFILE_SJ")
    MONA_CD: Union[str, int, float, None] = Field(None, description="국회의원코드", alias="MONA_CD")
    PROFILE_UNIT_CD: Union[str, int, float, None] = Field(None, description="경력대수코드", alias="PROFILE_UNIT_CD")
    PROFILE_UNIT_NM: Union[str, int, float, None] = Field(None, description="경력대수", alias="PROFILE_UNIT_NM")

class Params_OD21030011944P19666(BaseModel):
    """Request parameters for OD21030011944P19666"""
    HG_NM: str | None = Field(None, description="의원이름(한글)", alias="HG_NM")
    PROFILE_SJ: str | None = Field(None, description="의원이력", alias="PROFILE_SJ")
    MONA_CD: str | None = Field(None, description="국회의원코드", alias="MONA_CD")
    PROFILE_UNIT_CD: str = Field(..., description="경력대수코드", alias="PROFILE_UNIT_CD")

class Model_OOWY4R001216HX11462(BaseModel):
    """Response model for OOWY4R001216HX11462"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    PPSR_KIND: Union[str, int, float, None] = Field(None, description="제안자구분", alias="PPSR_KIND")
    PPSL_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PPSL_DT")
    JRCMIT_NM: Union[str, int, float, None] = Field(None, description="소관위원회명", alias="JRCMIT_NM")
    BDG_CMMT_DT: Union[str, int, float, None] = Field(None, description="소관위원회 회부일", alias="BDG_CMMT_DT")
    JRCMIT_PRSNT_DT: Union[str, int, float, None] = Field(None, description="소관위원회 상정일", alias="JRCMIT_PRSNT_DT")
    JRCMIT_PROC_DT: Union[str, int, float, None] = Field(None, description="소관위원회 처리일", alias="JRCMIT_PROC_DT")
    JRCMIT_PROC_RSLT: Union[str, int, float, None] = Field(None, description="소관위원회 처리결과", alias="JRCMIT_PROC_RSLT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11462(BaseModel):
    """Request parameters for OOWY4R001216HX11462"""
    ERACO: str | None = Field(None, description="대수", alias="ERACO")

class Model_OOWY4R001216HX11438(BaseModel):
    """Response model for OOWY4R001216HX11438"""
    DPLM_TRD_TTL: Union[str, int, float, None] = Field(None, description="의회외교 동향 제목", alias="DPLM_TRD_TTL")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일자", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 URL", alias="LINK_URL")

class Params_OOWY4R001216HX11438(BaseModel):
    """Request parameters for OOWY4R001216HX11438"""
    DPLM_TRD_TTL: str | None = Field(None, description="의회외교 동향 제목", alias="DPLM_TRD_TTL")

class Model_OOWY4R001216HX11437(BaseModel):
    """Response model for OOWY4R001216HX11437"""
    SCH_KIND: Union[str, int, float, None] = Field(None, description="일정종류", alias="SCH_KIND")
    SCH_CN: Union[str, int, float, None] = Field(None, description="일정내용", alias="SCH_CN")
    SCH_DT: Union[str, int, float, None] = Field(None, description="일자", alias="SCH_DT")
    SCH_TM: Union[str, int, float, None] = Field(None, description="시간", alias="SCH_TM")
    CONF_DIV: Union[str, int, float, None] = Field(None, description="회의구분", alias="CONF_DIV")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    CONF_SESS: Union[str, int, float, None] = Field(None, description="회의회기", alias="CONF_SESS")
    CONF_DGR: Union[str, int, float, None] = Field(None, description="회의차수", alias="CONF_DGR")
    EV_INST_NM: Union[str, int, float, None] = Field(None, description="행사주체자", alias="EV_INST_NM")
    EV_PLC: Union[str, int, float, None] = Field(None, description="행사장소", alias="EV_PLC")

class Params_OOWY4R001216HX11437(BaseModel):
    """Request parameters for OOWY4R001216HX11437"""
    SCH_KIND: str | None = Field(None, description="일정종류", alias="SCH_KIND")
    SCH_DT: str | None = Field(None, description="일자", alias="SCH_DT")

class Model_O5MSQF0009823A15643(BaseModel):
    """Response model for O5MSQF0009823A15643"""
    V_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="V_TITLE")
    URL_LINK: Union[str, int, float, None] = Field(None, description="기사 URL", alias="URL_LINK")
    DATE_LASTMODIFIED: Union[str, int, float, None] = Field(None, description="최종수정일", alias="DATE_LASTMODIFIED")
    DATE_RELEASED: Union[str, int, float, None] = Field(None, description="기사작성일", alias="DATE_RELEASED")
    V_BODY: Union[str, int, float, None] = Field(None, description="기사내용", alias="V_BODY")

class Params_O5MSQF0009823A15643(BaseModel):
    """Request parameters for O5MSQF0009823A15643"""
    V_TITLE: str | None = Field(None, description="제목", alias="V_TITLE")

class Model_OOWY4R001216HX11507(BaseModel):
    """Response model for OOWY4R001216HX11507"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    CONF_KND: Union[str, int, float, None] = Field(None, description="회의종류", alias="CONF_KND")
    CMIT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="CMIT_CD")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운로드 URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11507(BaseModel):
    """Request parameters for OOWY4R001216HX11507"""
    ERACO: str = Field(..., description="대수", alias="ERACO")
    CMIT_CD: str | None = Field(None, description="위원회코드", alias="CMIT_CD")

class Model_OB3OEN0011786012232(BaseModel):
    """Response model for OB3OEN0011786012232"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_OB3OEN0011786012232(BaseModel):
    """Request parameters for OB3OEN0011786012232"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_OTSI7L0011705B12017(BaseModel):
    """Response model for OTSI7L0011705B12017"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_OTSI7L0011705B12017(BaseModel):
    """Request parameters for OTSI7L0011705B12017"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_OAFHCY001008NN11647(BaseModel):
    """Response model for OAFHCY001008NN11647"""
    WRITER_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="WRITER_NM")
    ARTICLE_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="ARTICLE_TITLE")
    CREATE_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="CREATE_DT")
    DEPT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="DEPT_CD")

class Params_OAFHCY001008NN11647(BaseModel):
    """Request parameters for OAFHCY001008NN11647"""
    WRITER_NM: str | None = Field(None, description="위원회명", alias="WRITER_NM")
    ARTICLE_TITLE: str | None = Field(None, description="제목", alias="ARTICLE_TITLE")
    DEPT_CD: str | None = Field(None, description="위원회코드", alias="DEPT_CD")

class Model_OOWY4R001216HX11445(BaseModel):
    """Response model for OOWY4R001216HX11445"""
    SPC_TTL: Union[str, int, float, None] = Field(None, description="연설문 제목", alias="SPC_TTL")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일자", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11445(BaseModel):
    """Request parameters for OOWY4R001216HX11445"""
    SPC_TTL: str | None = Field(None, description="연설문 제목", alias="SPC_TTL")

class Model_OL39BM000986V214201(BaseModel):
    """Response model for OL39BM000986V214201"""
    V_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="V_TITLE")
    URL_LINK: Union[str, int, float, None] = Field(None, description="기사 URL", alias="URL_LINK")
    DATE_LASTMODIFIED: Union[str, int, float, None] = Field(None, description="최종수정일", alias="DATE_LASTMODIFIED")
    DATE_RELEASED: Union[str, int, float, None] = Field(None, description="기사작성일", alias="DATE_RELEASED")
    V_BODY: Union[str, int, float, None] = Field(None, description="기사내용", alias="V_BODY")

class Params_OL39BM000986V214201(BaseModel):
    """Request parameters for OL39BM000986V214201"""
    V_TITLE: str | None = Field(None, description="제목", alias="V_TITLE")

class Model_OXZDRJ0011169E17589(BaseModel):
    """Response model for OXZDRJ0011169E17589"""
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_OXZDRJ0011169E17589(BaseModel):
    """Request parameters for OXZDRJ0011169E17589"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: str | None = Field(None, description="등록일자", alias="INSERTDT")

class Model_OOWY4R001216HX11498(BaseModel):
    """Response model for OOWY4R001216HX11498"""
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    PPSR_KIND_NM: Union[str, int, float, None] = Field(None, description="제안자구분명", alias="PPSR_KIND_NM")
    PPSL_DT: Union[str, int, float, None] = Field(None, description="제안일자", alias="PPSL_DT")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    MSESS_RSLN_DT: Union[str, int, float, None] = Field(None, description="본회의의결일자", alias="MSESS_RSLN_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 URL", alias="LINK_URL")

class Params_OOWY4R001216HX11498(BaseModel):
    """Request parameters for OOWY4R001216HX11498"""
    BILL_NM: str | None = Field(None, description="의안명", alias="BILL_NM")

class Model_OOWY4R001216HX11477(BaseModel):
    """Response model for OOWY4R001216HX11477"""
    PRPSR_DIV_NM: Union[str, int, float, None] = Field(None, description="발의자구분명", alias="PRPSR_DIV_NM")
    RCP_CNT: Union[str, int, float, None] = Field(None, description="접수건수", alias="RCP_CNT")
    PROC_CNT: Union[str, int, float, None] = Field(None, description="처리건수", alias="PROC_CNT")
    REFT_SUBT: Union[str, int, float, None] = Field(None, description="반영소계", alias="REFT_SUBT")
    OBIL_PSSG_CNT: Union[str, int, float, None] = Field(None, description="원안가결건수", alias="OBIL_PSSG_CNT")
    AMND_PSSG_CNT: Union[str, int, float, None] = Field(None, description="수정안가결건수", alias="AMND_PSSG_CNT")
    ALTPL_REFT_CNT: Union[str, int, float, None] = Field(None, description="대안반영건수", alias="ALTPL_REFT_CNT")
    AMND_REFT_CNT: Union[str, int, float, None] = Field(None, description="수정안반영건수", alias="AMND_REFT_CNT")
    UN_REFT_SUBT: Union[str, int, float, None] = Field(None, description="미반영소계", alias="UN_REFT_SUBT")
    RJCTN_CNT: Union[str, int, float, None] = Field(None, description="부결건수", alias="RJCTN_CNT")
    DSU_CNT: Union[str, int, float, None] = Field(None, description="폐기건수", alias="DSU_CNT")
    WTHD_CNT: Union[str, int, float, None] = Field(None, description="철회건수", alias="WTHD_CNT")
    GVB_CNT: Union[str, int, float, None] = Field(None, description="반려건수", alias="GVB_CNT")
    ETC_CNT: Union[str, int, float, None] = Field(None, description="기타건수", alias="ETC_CNT")
    RSVT_CNT: Union[str, int, float, None] = Field(None, description="보류건수", alias="RSVT_CNT")

class Params_OOWY4R001216HX11477(BaseModel):
    """Request parameters for OOWY4R001216HX11477"""
    ERACO: str = Field(..., description="대수", alias="ERACO")

class Model_OOWY4R001216HX11432(BaseModel):
    """Response model for OOWY4R001216HX11432"""
    PBLM_TTL: Union[str, int, float, None] = Field(None, description="발간물 제목", alias="PBLM_TTL")
    WRT_DEPT: Union[str, int, float, None] = Field(None, description="작성부서", alias="WRT_DEPT")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11432(BaseModel):
    """Request parameters for OOWY4R001216HX11432"""
    PBLM_TTL: str | None = Field(None, description="발간물 제목", alias="PBLM_TTL")

class Model_OEQ77R000942NL11530(BaseModel):
    """Response model for OEQ77R000942NL11530"""
    REGDAESU: Union[str, int, float, None] = Field(None, description="대수", alias="REGDAESU")
    REPORT_TITLE: Union[str, int, float, None] = Field(None, description="보고서명", alias="REPORT_TITLE")
    YEAR: Union[str, int, float, None] = Field(None, description="연도", alias="YEAR")
    RE_NAME: Union[str, int, float, None] = Field(None, description="연구단체명", alias="RE_NAME")
    PDF_DOWN_URL: Union[str, int, float, None] = Field(None, description="", alias="PDF_DOWN_URL")
    REPORT_CLASSIFICATION_NM: Union[str, int, float, None] = Field(None, description="보고서분류", alias="REPORT_CLASSIFICATION_NM")

class Params_OEQ77R000942NL11530(BaseModel):
    """Request parameters for OEQ77R000942NL11530"""
    REGDAESU: str = Field(..., description="대수", alias="REGDAESU")
    REPORT_TITLE: str | None = Field(None, description="보고서명", alias="REPORT_TITLE")
    YEAR: str | None = Field(None, description="연도", alias="YEAR")
    RE_NAME: str | None = Field(None, description="연구단체명", alias="RE_NAME")

class Model_O2PLAU000882CD18776(BaseModel):
    """Response model for O2PLAU000882CD18776"""
    CTR_RDT: Union[str, int, float, None] = Field(None, description="계약일자", alias="CTR_RDT")
    CTR_NM: Union[str, int, float, None] = Field(None, description="계약건명", alias="CTR_NM")
    CTR_AMT: Union[str, int, float, None] = Field(None, description="계약금액(원)", alias="CTR_AMT")
    CTR_OJ_NM: Union[str, int, float, None] = Field(None, description="계약상대자", alias="CTR_OJ_NM")
    CTR_MTH: Union[str, int, float, None] = Field(None, description="계약방법", alias="CTR_MTH")

class Params_O2PLAU000882CD18776(BaseModel):
    """Request parameters for O2PLAU000882CD18776"""
    CTR_NM: str | None = Field(None, description="계약건명", alias="CTR_NM")
    CTR_OJ_NM: str | None = Field(None, description="계약상대자", alias="CTR_OJ_NM")
    CTR_MTH: str | None = Field(None, description="계약방법", alias="CTR_MTH")

class Model_OOWY4R001216HX11486(BaseModel):
    """Response model for OOWY4R001216HX11486"""
    PTT_ID: Union[str, int, float, None] = Field(None, description="청원ID", alias="PTT_ID")
    PTT_NO: Union[str, int, float, None] = Field(None, description="청원번호", alias="PTT_NO")
    PTTR_NM: Union[str, int, float, None] = Field(None, description="청원자명", alias="PTTR_NM")
    REP_DIV: Union[str, int, float, None] = Field(None, description="대표구분", alias="REP_DIV")
    INTD_ASBLM_NM: Union[str, int, float, None] = Field(None, description="소개의원명", alias="INTD_ASBLM_NM")

class Params_OOWY4R001216HX11486(BaseModel):
    """Request parameters for OOWY4R001216HX11486"""
    PTT_ID: str = Field(..., description="청원ID", alias="PTT_ID")

class Model_O5K6OC001166I215604(BaseModel):
    """Response model for O5K6OC001166I215604"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_O5K6OC001166I215604(BaseModel):
    """Request parameters for O5K6OC001166I215604"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_O27DU0000960M511942(BaseModel):
    """Response model for O27DU0000960M511942"""
    MEETING_DATE: Union[str, int, float, None] = Field(None, description="회의일자", alias="MEETING_DATE")
    MEETING_TIME: Union[str, int, float, None] = Field(None, description="시간", alias="MEETING_TIME")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DEGREE: Union[str, int, float, None] = Field(None, description="차수", alias="DEGREE")
    TITLE: Union[str, int, float, None] = Field(None, description="구분", alias="TITLE")
    COMMITTEE_NAME: Union[str, int, float, None] = Field(None, description="위원회 명", alias="COMMITTEE_NAME")
    LINK_URL2: Union[str, int, float, None] = Field(None, description="상세_URL", alias="LINK_URL2")
    UNIT_CD: Union[str, int, float, None] = Field(None, description="대수", alias="UNIT_CD")
    UNIT_NM: Union[str, int, float, None] = Field(None, description="대수", alias="UNIT_NM")
    HR_DEPT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="HR_DEPT_CD")
    ANGUN: Union[str, int, float, None] = Field(None, description="안건", alias="ANGUN")

class Params_O27DU0000960M511942(BaseModel):
    """Request parameters for O27DU0000960M511942"""
    MEETING_DATE: str | None = Field(None, description="회의일자", alias="MEETING_DATE")
    MEETING_TIME: str | None = Field(None, description="시간", alias="MEETING_TIME")
    SESS: str | None = Field(None, description="회기", alias="SESS")
    DEGREE: str | None = Field(None, description="차수", alias="DEGREE")
    TITLE: str | None = Field(None, description="구분", alias="TITLE")
    COMMITTEE_NAME: str | None = Field(None, description="위원회 명", alias="COMMITTEE_NAME")
    UNIT_CD: str = Field(..., description="대수", alias="UNIT_CD")
    HR_DEPT_CD: str | None = Field(None, description="위원회코드", alias="HR_DEPT_CD")

class Model_ODNHIU0010588P19122(BaseModel):
    """Response model for ODNHIU0010588P19122"""
    COMP_MAIN_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="COMP_MAIN_TITLE")
    REG_DATE: Union[str, int, float, None] = Field(None, description="등록일자", alias="REG_DATE")
    COMP_CONTENT: Union[str, int, float, None] = Field(None, description="내용", alias="COMP_CONTENT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="상세보기", alias="LINK_URL")

class Params_ODNHIU0010588P19122(BaseModel):
    """Request parameters for ODNHIU0010588P19122"""
    COMP_MAIN_TITLE: str | None = Field(None, description="제목", alias="COMP_MAIN_TITLE")
    REG_DATE: str = Field(..., description="등록일자", alias="REG_DATE")
    COMP_CONTENT: str | None = Field(None, description="내용", alias="COMP_CONTENT")

class Model_OOWY4R001216HX11436(BaseModel):
    """Response model for OOWY4R001216HX11436"""
    DPLM_WORD: Union[str, int, float, None] = Field(None, description="의회외교 단어", alias="DPLM_WORD")
    DPLM_WORD_EN: Union[str, int, float, None] = Field(None, description="의회외교 영문단어", alias="DPLM_WORD_EN")

class Params_OOWY4R001216HX11436(BaseModel):
    """Request parameters for OOWY4R001216HX11436"""
    DPLM_WORD: str | None = Field(None, description="의회외교 단어", alias="DPLM_WORD")

class Model_O7RUVD001183U610140(BaseModel):
    """Response model for O7RUVD001183U610140"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")

class Params_O7RUVD001183U610140(BaseModel):
    """Request parameters for O7RUVD001183U610140"""
    REG_DATE: str | None = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_OR0YT0001112TD13067(BaseModel):
    """Response model for OR0YT0001112TD13067"""
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_OR0YT0001112TD13067(BaseModel):
    """Request parameters for OR0YT0001112TD13067"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: str | None = Field(None, description="등록일자", alias="INSERTDT")

class Model_OKDE3A001150P113085(BaseModel):
    """Response model for OKDE3A001150P113085"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    DIV: Union[str, int, float, None] = Field(None, description="구분", alias="DIV")
    NEWELCT: Union[str, int, float, None] = Field(None, description="초선", alias="NEWELCT")
    TWOTERM: Union[str, int, float, None] = Field(None, description="2선", alias="TWOTERM")
    THRTERM: Union[str, int, float, None] = Field(None, description="3선", alias="THRTERM")
    FOURTERM: Union[str, int, float, None] = Field(None, description="4선", alias="FOURTERM")
    FIVTERM: Union[str, int, float, None] = Field(None, description="5선", alias="FIVTERM")
    SIXTERM: Union[str, int, float, None] = Field(None, description="6선", alias="SIXTERM")
    SEVTERM: Union[str, int, float, None] = Field(None, description="7선", alias="SEVTERM")
    EIGTERM: Union[str, int, float, None] = Field(None, description="8선", alias="EIGTERM")
    NINTERM: Union[str, int, float, None] = Field(None, description="9선", alias="NINTERM")
    YEARPECT: Union[str, int, float, None] = Field(None, description="연인원수", alias="YEARPECT")

class Params_OKDE3A001150P113085(BaseModel):
    """Request parameters for OKDE3A001150P113085"""
    ERACO: str | None = Field(None, description="대수", alias="ERACO")
    DIV: str | None = Field(None, description="구분", alias="DIV")

class Model_O3VTTM0010223D15681(BaseModel):
    """Response model for O3VTTM0010223D15681"""
    CT1: Union[str, int, float, None] = Field(None, description="대수", alias="CT1")
    CT2: Union[str, int, float, None] = Field(None, description="회", alias="CT2")
    CT3: Union[str, int, float, None] = Field(None, description="차", alias="CT3")
    TAKING_DATE: Union[str, int, float, None] = Field(None, description="회의일자", alias="TAKING_DATE")
    TITLE: Union[str, int, float, None] = Field(None, description="회의제목", alias="TITLE")
    ESSENTIAL_PERSON: Union[str, int, float, None] = Field(None, description="발언자", alias="ESSENTIAL_PERSON")
    REC_TIME: Union[str, int, float, None] = Field(None, description="재생시간", alias="REC_TIME")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크주소", alias="LINK_URL")

class Params_O3VTTM0010223D15681(BaseModel):
    """Request parameters for O3VTTM0010223D15681"""
    CT1: str = Field(..., description="대수", alias="CT1")
    TAKING_DATE: str = Field(..., description="회의일자", alias="TAKING_DATE")
    TITLE: str | None = Field(None, description="회의제목", alias="TITLE")
    ESSENTIAL_PERSON: str | None = Field(None, description="발언자", alias="ESSENTIAL_PERSON")

class Model_OOWY4R001216HX11523(BaseModel):
    """Response model for OOWY4R001216HX11523"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    FILE_CN: Union[str, int, float, None] = Field(None, description="파일설명", alias="FILE_CN")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11523(BaseModel):
    """Request parameters for OOWY4R001216HX11523"""
    CONF_ID: str | None = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: str | None = Field(None, description="대수", alias="ERACO")

class Model_O0MH4O001149BH11948(BaseModel):
    """Response model for O0MH4O001149BH11948"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    PLPT_NM: Union[str, int, float, None] = Field(None, description="정당명", alias="PLPT_NM")
    SEOUL: Union[str, int, float, None] = Field(None, description="서울", alias="SEOUL")
    BUSAN: Union[str, int, float, None] = Field(None, description="부산", alias="BUSAN")
    DEAGU: Union[str, int, float, None] = Field(None, description="대구", alias="DEAGU")
    INCHUN: Union[str, int, float, None] = Field(None, description="인천", alias="INCHUN")
    GWANGJU: Union[str, int, float, None] = Field(None, description="광주", alias="GWANGJU")
    DEAJUN: Union[str, int, float, None] = Field(None, description="대전", alias="DEAJUN")
    ULSAN: Union[str, int, float, None] = Field(None, description="울산", alias="ULSAN")
    SEJONG: Union[str, int, float, None] = Field(None, description="세종", alias="SEJONG")
    GYUNGGI: Union[str, int, float, None] = Field(None, description="경기", alias="GYUNGGI")
    GANGWON: Union[str, int, float, None] = Field(None, description="강원", alias="GANGWON")
    CHUNGBUK: Union[str, int, float, None] = Field(None, description="충북", alias="CHUNGBUK")
    CHUNGNAM: Union[str, int, float, None] = Field(None, description="충남", alias="CHUNGNAM")
    JUNBUK: Union[str, int, float, None] = Field(None, description="전북", alias="JUNBUK")
    JUNNAM: Union[str, int, float, None] = Field(None, description="전남", alias="JUNNAM")
    KYUNGBUK: Union[str, int, float, None] = Field(None, description="경북", alias="KYUNGBUK")
    KYUNGNAM: Union[str, int, float, None] = Field(None, description="경남", alias="KYUNGNAM")
    JEJU: Union[str, int, float, None] = Field(None, description="제주", alias="JEJU")
    TNCFUCT: Union[str, int, float, None] = Field(None, description="통일주체국민회의", alias="TNCFUCT")
    PRPR: Union[str, int, float, None] = Field(None, description="비례", alias="PRPR")
    SUM: Union[str, int, float, None] = Field(None, description="합계", alias="SUM")
    RMK: Union[str, int, float, None] = Field(None, description="비고", alias="RMK")

class Params_O0MH4O001149BH11948(BaseModel):
    """Request parameters for O0MH4O001149BH11948"""
    ERACO: str | None = Field(None, description="대수", alias="ERACO")
    PLPT_NM: str | None = Field(None, description="정당명", alias="PLPT_NM")

class Model_OOWY4R001216HX11418(BaseModel):
    """Response model for OOWY4R001216HX11418"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    PPSL_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PPSL_DT")
    RGS_PRSNT_DT: Union[str, int, float, None] = Field(None, description="본회의 심의 상정일", alias="RGS_PRSNT_DT")
    RGS_RSLN_DT: Union[str, int, float, None] = Field(None, description="본회의 심의 의결일", alias="RGS_RSLN_DT")
    HWP_DWLD_URL: Union[str, int, float, None] = Field(None, description="PDF 다운 URL", alias="HWP_DWLD_URL")
    PDF_DWLD_URL: Union[str, int, float, None] = Field(None, description="HWP 다운 URL", alias="PDF_DWLD_URL")

class Params_OOWY4R001216HX11418(BaseModel):
    """Request parameters for OOWY4R001216HX11418"""
    BILL_NM: str | None = Field(None, description="의안명", alias="BILL_NM")

class Model_O927U9001135M913005(BaseModel):
    """Response model for O927U9001135M913005"""
    TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="TITLE")
    PUBLISHER: Union[str, int, float, None] = Field(None, description="발행처", alias="PUBLISHER")
    DETAIL_VIEW_URL: Union[str, int, float, None] = Field(None, description="상세보기URL", alias="DETAIL_VIEW_URL")
    UPDATE_DT: Union[str, int, float, None] = Field(None, description="수정일", alias="UPDATE_DT")
    PUBLISH_DT: Union[str, int, float, None] = Field(None, description="발행년", alias="PUBLISH_DT")

class Params_O927U9001135M913005(BaseModel):
    """Request parameters for O927U9001135M913005"""
    TITLE: str | None = Field(None, description="제목", alias="TITLE")
    PUBLISHER: str | None = Field(None, description="발행처", alias="PUBLISHER")
    UPDATE_DT: str | None = Field(None, description="수정일", alias="UPDATE_DT")
    PUBLISH_DT: str | None = Field(None, description="발행년", alias="PUBLISH_DT")

class Model_OVW2NU000937WK15521(BaseModel):
    """Response model for OVW2NU000937WK15521"""
    DAE_NUM: Union[str, int, float, None] = Field(None, description="대수", alias="DAE_NUM")
    SES_NUM: Union[str, int, float, None] = Field(None, description="회기", alias="SES_NUM")
    DEGREE_NUM: Union[str, int, float, None] = Field(None, description="차수", alias="DEGREE_NUM")
    COMM_NAME: Union[str, int, float, None] = Field(None, description="위원회", alias="COMM_NAME")
    CONF_DATE: Union[str, int, float, None] = Field(None, description="회의일", alias="CONF_DATE")
    BILL_URL: Union[str, int, float, None] = Field(None, description="안건보기", alias="BILL_URL")
    CLASS_NAME: Union[str, int, float, None] = Field(None, description="회의종류", alias="CLASS_NAME")

class Params_OVW2NU000937WK15521(BaseModel):
    """Request parameters for OVW2NU000937WK15521"""
    DAE_NUM: str = Field(..., description="대수", alias="DAE_NUM")
    SES_NUM: str | None = Field(None, description="회기", alias="SES_NUM")
    DEGREE_NUM: str | None = Field(None, description="차수", alias="DEGREE_NUM")
    COMM_NAME: str | None = Field(None, description="위원회", alias="COMM_NAME")
    CONF_DATE: str | None = Field(None, description="회의일", alias="CONF_DATE")
    CLASS_NAME: str | None = Field(None, description="회의종류", alias="CLASS_NAME")

class Model_OOWY4R001216HX11440(BaseModel):
    """Response model for OOWY4R001216HX11440"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_KND: Union[str, int, float, None] = Field(None, description="의안종류", alias="BILL_KND")
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    PPSR_KND: Union[str, int, float, None] = Field(None, description="제안자구분", alias="PPSR_KND")
    PPSR_NM: Union[str, int, float, None] = Field(None, description="제안자명", alias="PPSR_NM")
    PPSL_SESS: Union[str, int, float, None] = Field(None, description="제안회기", alias="PPSL_SESS")
    PPSL_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PPSL_DT")
    JRCMIT_NM: Union[str, int, float, None] = Field(None, description="소관위원회명", alias="JRCMIT_NM")
    JRCMIT_CMMT_DT: Union[str, int, float, None] = Field(None, description="소관위원회 회부일", alias="JRCMIT_CMMT_DT")
    JRCMIT_PRSNT_DT: Union[str, int, float, None] = Field(None, description="소관위원회 상정일", alias="JRCMIT_PRSNT_DT")
    JRCMIT_PROC_DT: Union[str, int, float, None] = Field(None, description="소관위원회 처리일", alias="JRCMIT_PROC_DT")
    JRCMIT_PROC_RSLT: Union[str, int, float, None] = Field(None, description="소관위원회 처리결과", alias="JRCMIT_PROC_RSLT")
    LAW_CMMT_DT: Union[str, int, float, None] = Field(None, description="법사위 체계자구심사 회부일", alias="LAW_CMMT_DT")
    LAW_PRSNT_DT: Union[str, int, float, None] = Field(None, description="법사위 체계자구심사 상정일", alias="LAW_PRSNT_DT")
    LAW_PROC_DT: Union[str, int, float, None] = Field(None, description="법사위 체계자구심사 처리일", alias="LAW_PROC_DT")
    LAW_PROC_RSLT: Union[str, int, float, None] = Field(None, description="법사위 체계자구심사 처리결과", alias="LAW_PROC_RSLT")
    RGS_PRSNT_DT: Union[str, int, float, None] = Field(None, description="본회의 심의 상정일", alias="RGS_PRSNT_DT")
    RGS_RSLN_DT: Union[str, int, float, None] = Field(None, description="본회의 심의 의결일", alias="RGS_RSLN_DT")
    RGS_CONF_NM: Union[str, int, float, None] = Field(None, description="본회의 심의 회의명", alias="RGS_CONF_NM")
    RGS_CONF_RSLT: Union[str, int, float, None] = Field(None, description="본회의 심의결과", alias="RGS_CONF_RSLT")
    GVRN_TRSF_DT: Union[str, int, float, None] = Field(None, description="정부 이송일", alias="GVRN_TRSF_DT")
    PROM_LAW_NM: Union[str, int, float, None] = Field(None, description="공포 법률명", alias="PROM_LAW_NM")
    PROM_DT: Union[str, int, float, None] = Field(None, description="공포일", alias="PROM_DT")
    PROM_NO: Union[str, int, float, None] = Field(None, description="공포번호", alias="PROM_NO")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11440(BaseModel):
    """Request parameters for OOWY4R001216HX11440"""
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: str = Field(..., description="의안번호", alias="BILL_NO")
    BILL_KND: str | None = Field(None, description="의안종류", alias="BILL_KND")
    BILL_NM: str | None = Field(None, description="의안명", alias="BILL_NM")
    PPSR_KND: str | None = Field(None, description="제안자구분", alias="PPSR_KND")
    PPSL_DT: str | None = Field(None, description="제안일", alias="PPSL_DT")
    JRCMIT_NM: str | None = Field(None, description="소관위원회명", alias="JRCMIT_NM")
    RGS_CONF_RSLT: str | None = Field(None, description="본회의 심의결과", alias="RGS_CONF_RSLT")

class Model_O78HKE0010099W15881(BaseModel):
    """Response model for O78HKE0010099W15881"""
    REGDAESU: Union[str, int, float, None] = Field(None, description="대수", alias="REGDAESU")
    RE_TOPIC_NAME: Union[str, int, float, None] = Field(None, description="분야별", alias="RE_TOPIC_NAME")
    RE_NAME: Union[str, int, float, None] = Field(None, description="연구단체", alias="RE_NAME")
    RE_OBJECTIVE: Union[str, int, float, None] = Field(None, description="연구목적", alias="RE_OBJECTIVE")
    MAIN_MEM: Union[str, int, float, None] = Field(None, description="대표의원", alias="MAIN_MEM")
    RE_MEM: Union[str, int, float, None] = Field(None, description="연구책임의원", alias="RE_MEM")
    OBJ_MEM: Union[str, int, float, None] = Field(None, description="구성의원", alias="OBJ_MEM")
    MEMBER_CNT: Union[str, int, float, None] = Field(None, description="구성인원", alias="MEMBER_CNT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크주소", alias="LINK_URL")

class Params_O78HKE0010099W15881(BaseModel):
    """Request parameters for O78HKE0010099W15881"""
    REGDAESU: str = Field(..., description="대수", alias="REGDAESU")
    RE_TOPIC_NAME: str | None = Field(None, description="분야별", alias="RE_TOPIC_NAME")
    RE_NAME: str | None = Field(None, description="연구단체", alias="RE_NAME")
    RE_OBJECTIVE: str | None = Field(None, description="연구목적", alias="RE_OBJECTIVE")
    MAIN_MEM: str | None = Field(None, description="대표의원", alias="MAIN_MEM")
    RE_MEM: str | None = Field(None, description="연구책임의원", alias="RE_MEM")
    OBJ_MEM: str | None = Field(None, description="구성의원", alias="OBJ_MEM")

class Model_OP7W8M000944IF15092(BaseModel):
    """Response model for OP7W8M000944IF15092"""
    NOTICE_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="NOTICE_TITLE")
    DEPT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPT_NAME")
    WRITE_DATE: Union[str, int, float, None] = Field(None, description="작성일", alias="WRITE_DATE")
    NOTICE_NM: Union[str, int, float, None] = Field(None, description="구분명", alias="NOTICE_NM")
    CONTENT: Union[str, int, float, None] = Field(None, description="내용", alias="CONTENT")
    PDF_FILE_URL: Union[str, int, float, None] = Field(None, description="PDF첨부파일경로", alias="PDF_FILE_URL")
    ATTACH_FILE_URL: Union[str, int, float, None] = Field(None, description="첨부파일경로", alias="ATTACH_FILE_URL")

class Params_OP7W8M000944IF15092(BaseModel):
    """Request parameters for OP7W8M000944IF15092"""
    NOTICE_TITLE: str | None = Field(None, description="제목", alias="NOTICE_TITLE")
    DEPT_NAME: str | None = Field(None, description="부서명", alias="DEPT_NAME")
    WRITE_DATE: str | None = Field(None, description="작성일", alias="WRITE_DATE")
    CONTENT: str | None = Field(None, description="내용", alias="CONTENT")

class Model_OB5IBW001180FQ10640(BaseModel):
    """Response model for OB5IBW001180FQ10640"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_OB5IBW001180FQ10640(BaseModel):
    """Request parameters for OB5IBW001180FQ10640"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_O4BV430009830710440(BaseModel):
    """Response model for O4BV430009830710440"""
    V_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="V_TITLE")
    URL_LINK: Union[str, int, float, None] = Field(None, description="기사 URL", alias="URL_LINK")
    DATE_LASTMODIFIED: Union[str, int, float, None] = Field(None, description="최종수정일", alias="DATE_LASTMODIFIED")
    DATE_RELEASED: Union[str, int, float, None] = Field(None, description="기사작성일", alias="DATE_RELEASED")
    V_BODY: Union[str, int, float, None] = Field(None, description="기사내용", alias="V_BODY")

class Params_O4BV430009830710440(BaseModel):
    """Request parameters for O4BV430009830710440"""
    V_TITLE: str | None = Field(None, description="제목", alias="V_TITLE")

class Model_OU8JBT0015343C14378(BaseModel):
    """Response model for OU8JBT0015343C14378"""
    TH: Union[str, int, float, None] = Field(None, description="대수", alias="TH")
    CLASS_ID: Union[str, int, float, None] = Field(None, description="회의종류", alias="CLASS_ID")
    CLASS_NM: Union[str, int, float, None] = Field(None, description="회의종류명", alias="CLASS_NM")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    CMIT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="CMIT_CD")
    SUB_CMIT_CD: Union[str, int, float, None] = Field(None, description="소위원회코드", alias="SUB_CMIT_CD")
    SUB_CMIT_NM: Union[str, int, float, None] = Field(None, description="소위원회명", alias="SUB_CMIT_NM")

class Params_OU8JBT0015343C14378(BaseModel):
    """Request parameters for OU8JBT0015343C14378"""
    TH: str | None = Field(None, description="대수", alias="TH")
    CLASS_ID: str | None = Field(None, description="회의종류", alias="CLASS_ID")
    CMIT_NM: str | None = Field(None, description="위원회명", alias="CMIT_NM")

class Model_OMYCKJ0011621210030(BaseModel):
    """Response model for OMYCKJ0011621210030"""
    ARTICLE_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="ARTICLE_TITLE")
    WRITER_NM: Union[str, int, float, None] = Field(None, description="작성자", alias="WRITER_NM")
    CATEGORY_NM: Union[str, int, float, None] = Field(None, description="구분", alias="CATEGORY_NM")
    CREATE_DT: Union[str, int, float, None] = Field(None, description="등록일", alias="CREATE_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="상세보기URL", alias="LINK_URL")

class Params_OMYCKJ0011621210030(BaseModel):
    """Request parameters for OMYCKJ0011621210030"""
    ARTICLE_TITLE: str | None = Field(None, description="제목", alias="ARTICLE_TITLE")
    CATEGORY_NM: str | None = Field(None, description="구분", alias="CATEGORY_NM")

class Model_OOWY4R001216HX11512(BaseModel):
    """Response model for OOWY4R001216HX11512"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    CONF_KND: Union[str, int, float, None] = Field(None, description="회의종류", alias="CONF_KND")
    CMIT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="CMIT_CD")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운로드 URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11512(BaseModel):
    """Request parameters for OOWY4R001216HX11512"""
    ERACO: str = Field(..., description="대수", alias="ERACO")
    CMIT_CD: str | None = Field(None, description="위원회코드", alias="CMIT_CD")

class Model_OOWY4R001216HX11492(BaseModel):
    """Response model for OOWY4R001216HX11492"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    PPSR: Union[str, int, float, None] = Field(None, description="제안자", alias="PPSR")
    PPSL_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PPSL_DT")
    JRCMIT_CONF_NM: Union[str, int, float, None] = Field(None, description="소관위원회 심사 회의명", alias="JRCMIT_CONF_NM")
    JRCMIT_CONF_DT: Union[str, int, float, None] = Field(None, description="소관위원회 심사 회의일", alias="JRCMIT_CONF_DT")
    JRCMIT_CONF_RSLT: Union[str, int, float, None] = Field(None, description="소관위원회 심사 회의결과", alias="JRCMIT_CONF_RSLT")

class Params_OOWY4R001216HX11492(BaseModel):
    """Request parameters for OOWY4R001216HX11492"""
    BILL_ID: str = Field(..., description="의안ID", alias="BILL_ID")

class Model_OQ0A0T0011366V19103(BaseModel):
    """Response model for OQ0A0T0011366V19103"""
    TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="TITLE")
    SEMINAR_DIV_CODE: Union[str, int, float, None] = Field(None, description="구분", alias="SEMINAR_DIV_CODE")
    HOST_DT: Union[str, int, float, None] = Field(None, description="개최일시", alias="HOST_DT")
    HOST_PLACE_NAME: Union[str, int, float, None] = Field(None, description="장소", alias="HOST_PLACE_NAME")
    HOST_INS_NAME: Union[str, int, float, None] = Field(None, description="주최", alias="HOST_INS_NAME")
    ATTENDANCE_NAME1: Union[str, int, float, None] = Field(None, description="발제자", alias="ATTENDANCE_NAME1")
    ATTENDANCE_NAME2: Union[str, int, float, None] = Field(None, description="토론자", alias="ATTENDANCE_NAME2")
    DETAIL_VIEW_URL: Union[str, int, float, None] = Field(None, description="상세보기URL", alias="DETAIL_VIEW_URL")

class Params_OQ0A0T0011366V19103(BaseModel):
    """Request parameters for OQ0A0T0011366V19103"""
    TITLE: str | None = Field(None, description="제목", alias="TITLE")
    HOST_DT: str = Field(..., description="개최일시", alias="HOST_DT")
    HOST_INS_NAME: str | None = Field(None, description="주최", alias="HOST_INS_NAME")
    ATTENDANCE_NAME1: str | None = Field(None, description="발제자", alias="ATTENDANCE_NAME1")
    ATTENDANCE_NAME2: str | None = Field(None, description="토론자", alias="ATTENDANCE_NAME2")

class Model_OOWY4R001216HX11479(BaseModel):
    """Response model for OOWY4R001216HX11479"""
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    CONSTI_RFBIL_CNT: Union[str, int, float, None] = Field(None, description="헌법개정안건수", alias="CONSTI_RFBIL_CNT")
    DRFBD_CNT: Union[str, int, float, None] = Field(None, description="예산안건수", alias="DRFBD_CNT")
    STL_CNT: Union[str, int, float, None] = Field(None, description="결산건수", alias="STL_CNT")
    LGSLB_ASBLM_PRPSR_CNT: Union[str, int, float, None] = Field(None, description="법률안의원발의건수", alias="LGSLB_ASBLM_PRPSR_CNT")
    LGSLB_GVRN_PRPSR_CNT: Union[str, int, float, None] = Field(None, description="법률안정부발의건수", alias="LGSLB_GVRN_PRPSR_CNT")
    LGSLB_SUM: Union[str, int, float, None] = Field(None, description="법률안합계", alias="LGSLB_SUM")
    AGMB_CNT: Union[str, int, float, None] = Field(None, description="동의안건수", alias="AGMB_CNT")
    RSLNB_CNT: Union[str, int, float, None] = Field(None, description="결의안건수", alias="RSLNB_CNT")
    PRPSTB_CNT: Union[str, int, float, None] = Field(None, description="건의안건수", alias="PRPSTB_CNT")
    RULB_CNT: Union[str, int, float, None] = Field(None, description="규칙안 건수", alias="RULB_CNT")
    ELCTB_CNT: Union[str, int, float, None] = Field(None, description="선출안 건수", alias="ELCTB_CNT")
    IMPT_AGM_CNT: Union[str, int, float, None] = Field(None, description="중요동의 건수", alias="IMPT_AGM_CNT")
    CMTM_DSCP_CNT: Union[str, int, float, None] = Field(None, description="의원징계 건수", alias="CMTM_DSCP_CNT")
    CMTM_QLF_INSC_CNT: Union[str, int, float, None] = Field(None, description="의원자격심사 건수", alias="CMTM_QLF_INSC_CNT")
    ETC_CNT: Union[str, int, float, None] = Field(None, description="기타건수", alias="ETC_CNT")
    CMIT_BY_SUM: Union[str, int, float, None] = Field(None, description="위원회별합계", alias="CMIT_BY_SUM")

class Params_OOWY4R001216HX11479(BaseModel):
    """Request parameters for OOWY4R001216HX11479"""
    pass

class Model_OT9767000930ZL12696(BaseModel):
    """Response model for OT9767000930ZL12696"""
    FSCL_YY: Union[str, int, float, None] = Field(None, description="회계년도", alias="FSCL_YY")
    EXE_M: Union[str, int, float, None] = Field(None, description="회계월", alias="EXE_M")
    FSCL_NM: Union[str, int, float, None] = Field(None, description="회계명", alias="FSCL_NM")
    IKWAN_NM: Union[str, int, float, None] = Field(None, description="수입관명", alias="IKWAN_NM")
    IHANG_NM: Union[str, int, float, None] = Field(None, description="수입항명", alias="IHANG_NM")
    BDG_AMT: Union[str, int, float, None] = Field(None, description="예산금액", alias="BDG_AMT")
    RC_AGGR_AMT: Union[str, int, float, None] = Field(None, description="수납누계금액", alias="RC_AGGR_AMT")
    RC_AMT: Union[str, int, float, None] = Field(None, description="당월수납금액", alias="RC_AMT")

class Params_OT9767000930ZL12696(BaseModel):
    """Request parameters for OT9767000930ZL12696"""
    FSCL_YY: str | None = Field(None, description="회계년도", alias="FSCL_YY")
    EXE_M: str | None = Field(None, description="회계월", alias="EXE_M")
    FSCL_NM: str | None = Field(None, description="회계명", alias="FSCL_NM")
    IKWAN_NM: str | None = Field(None, description="수입관명", alias="IKWAN_NM")
    IHANG_NM: str | None = Field(None, description="수입항명", alias="IHANG_NM")

class Model_OS46YD0012559515463(BaseModel):
    """Response model for OS46YD0012559515463"""
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NAME")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    SUMMARY: Union[str, int, float, None] = Field(None, description="주요내용", alias="SUMMARY")
    AGE: Union[str, int, float, None] = Field(None, description="대수", alias="AGE")

class Params_OS46YD0012559515463(BaseModel):
    """Request parameters for OS46YD0012559515463"""
    BILL_NO: str = Field(..., description="의안번호", alias="BILL_NO")

class Model_OTICJI000959B917394(BaseModel):
    """Response model for OTICJI000959B917394"""
    BILL_NO: Union[str, int, float, None] = Field(None, description="청원번호", alias="BILL_NO")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    AGE: Union[str, int, float, None] = Field(None, description="대", alias="AGE")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="청원명", alias="BILL_NAME")
    PROPOSER: Union[str, int, float, None] = Field(None, description="청원인", alias="PROPOSER")
    APPROVER: Union[str, int, float, None] = Field(None, description="소개의원", alias="APPROVER")
    PROPOSE_DT: Union[str, int, float, None] = Field(None, description="접수일자", alias="PROPOSE_DT")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위", alias="CURR_COMMITTEE")
    COMMITTEE_DT: Union[str, int, float, None] = Field(None, description="위원회회부일", alias="COMMITTEE_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="상세보기URL", alias="LINK_URL")

class Params_OTICJI000959B917394(BaseModel):
    """Request parameters for OTICJI000959B917394"""
    BILL_NO: str | None = Field(None, description="청원번호", alias="BILL_NO")
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NAME: str | None = Field(None, description="청원명", alias="BILL_NAME")
    PROPOSER: str | None = Field(None, description="청원인", alias="PROPOSER")
    APPROVER: str | None = Field(None, description="소개의원", alias="APPROVER")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: str | None = Field(None, description="소관위", alias="CURR_COMMITTEE")
    PASS_GUBUN: str | None = Field(None, description="의안구분", alias="PASS_GUBUN")

class Model_OOWY4R001216HX11435(BaseModel):
    """Response model for OOWY4R001216HX11435"""
    PBLM_TTL: Union[str, int, float, None] = Field(None, description="발간물 제목", alias="PBLM_TTL")
    WRT_DEPT: Union[str, int, float, None] = Field(None, description="작성부서", alias="WRT_DEPT")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11435(BaseModel):
    """Request parameters for OOWY4R001216HX11435"""
    PBLM_TTL: str | None = Field(None, description="발간물 제목", alias="PBLM_TTL")

class Model_OJ24FX001003FD16907(BaseModel):
    """Response model for OJ24FX001003FD16907"""
    POLY_GROUP_NM: Union[str, int, float, None] = Field(None, description="교섭단체", alias="POLY_GROUP_NM")
    POLY_NM: Union[str, int, float, None] = Field(None, description="정당명", alias="POLY_NM")
    N1: Union[str, int, float, None] = Field(None, description="지역구", alias="N1")
    N2: Union[str, int, float, None] = Field(None, description="비례대표", alias="N2")
    N3: Union[str, int, float, None] = Field(None, description="계", alias="N3")
    N4: Union[str, int, float, None] = Field(None, description="비고(%)", alias="N4")

class Params_OJ24FX001003FD16907(BaseModel):
    """Request parameters for OJ24FX001003FD16907"""
    POLY_GROUP_NM: str | None = Field(None, description="교섭단체", alias="POLY_GROUP_NM")
    POLY_NM: str | None = Field(None, description="정당명", alias="POLY_NM")

class Model_OLH92R0011733J15777(BaseModel):
    """Response model for OLH92R0011733J15777"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_OLH92R0011733J15777(BaseModel):
    """Request parameters for OLH92R0011733J15777"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_OH473Z0011245H13792(BaseModel):
    """Response model for OH473Z0011245H13792"""
    PRDC_YM_NM: Union[str, int, float, None] = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: Union[str, int, float, None] = Field(None, description="공개파일명", alias="OPB_FL_NM")
    INST_CD: Union[str, int, float, None] = Field(None, description="기관코드", alias="INST_CD")
    INST_NM: Union[str, int, float, None] = Field(None, description="기관명", alias="INST_NM")
    OPB_FL_PH: Union[str, int, float, None] = Field(None, description="공개파일경로", alias="OPB_FL_PH")
    FILE_ID: Union[str, int, float, None] = Field(None, description="첨부파일ID", alias="FILE_ID")

class Params_OH473Z0011245H13792(BaseModel):
    """Request parameters for OH473Z0011245H13792"""
    pass

class Model_OOWY4R001216HX11475(BaseModel):
    """Response model for OOWY4R001216HX11475"""
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    RCP_CNT: Union[str, int, float, None] = Field(None, description="헌법개정안건수", alias="RCP_CNT")
    PROC_CNT: Union[str, int, float, None] = Field(None, description="예산안건수", alias="PROC_CNT")
    REFT_SUBT: Union[str, int, float, None] = Field(None, description="동의안건수", alias="REFT_SUBT")
    OBIL_PSSG_CNT: Union[str, int, float, None] = Field(None, description="결산건수", alias="OBIL_PSSG_CNT")
    AMND_PSSG_CNT: Union[str, int, float, None] = Field(None, description="법률안의원발의건수", alias="AMND_PSSG_CNT")
    ALTPL_REFT_CNT: Union[str, int, float, None] = Field(None, description="법률안정부발의건수", alias="ALTPL_REFT_CNT")
    AMND_REFT_CNT: Union[str, int, float, None] = Field(None, description="법률안합계", alias="AMND_REFT_CNT")
    UN_REFT_SUBT: Union[str, int, float, None] = Field(None, description="의원징계건수", alias="UN_REFT_SUBT")
    RJCTN_CNT: Union[str, int, float, None] = Field(None, description="결의안건수", alias="RJCTN_CNT")
    DSU_CNT: Union[str, int, float, None] = Field(None, description="건의안건수", alias="DSU_CNT")
    WTHD_CNT: Union[str, int, float, None] = Field(None, description="규칙안건수", alias="WTHD_CNT")
    GVB_CNT: Union[str, int, float, None] = Field(None, description="선출안건수", alias="GVB_CNT")
    ETC_CNT: Union[str, int, float, None] = Field(None, description="중요동의건수", alias="ETC_CNT")
    RSVT_CNT: Union[str, int, float, None] = Field(None, description="의원자격심사건수", alias="RSVT_CNT")

class Params_OOWY4R001216HX11475(BaseModel):
    """Request parameters for OOWY4R001216HX11475"""
    ERACO: str = Field(..., description="대수", alias="ERACO")

class Model_O8FQ4U000888KF14544(BaseModel):
    """Response model for O8FQ4U000888KF14544"""
    FCLT_NM: Union[str, int, float, None] = Field(None, description="시설물명", alias="FCLT_NM")
    YY_ARE: Union[str, int, float, None] = Field(None, description="연면적", alias="YY_ARE")
    ARCTC_ARE: Union[str, int, float, None] = Field(None, description="건축면적", alias="ARCTC_ARE")
    FLOR_SZ: Union[str, int, float, None] = Field(None, description="층수(지상/지하)", alias="FLOR_SZ")
    COMPLTN_DYS: Union[str, int, float, None] = Field(None, description="준공년월일", alias="COMPLTN_DYS")
    RMK: Union[str, int, float, None] = Field(None, description="비고", alias="RMK")

class Params_O8FQ4U000888KF14544(BaseModel):
    """Request parameters for O8FQ4U000888KF14544"""
    FCLT_NM: str | None = Field(None, description="시설물명", alias="FCLT_NM")
    COMPLTN_DYS: str | None = Field(None, description="준공년월일", alias="COMPLTN_DYS")

class Model_O6HDE2001161LX18191(BaseModel):
    """Response model for O6HDE2001161LX18191"""
    ARTICLE_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="ARTICLE_TITLE")
    WRITER_NM: Union[str, int, float, None] = Field(None, description="작성자", alias="WRITER_NM")
    CATEGORY_ID: Union[str, int, float, None] = Field(None, description="분류번호", alias="CATEGORY_ID")
    CATEGORY_NM: Union[str, int, float, None] = Field(None, description="구분", alias="CATEGORY_NM")
    CREATE_DT: Union[str, int, float, None] = Field(None, description="등록일", alias="CREATE_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="상세보기URL", alias="LINK_URL")

class Params_O6HDE2001161LX18191(BaseModel):
    """Request parameters for O6HDE2001161LX18191"""
    ARTICLE_TITLE: str | None = Field(None, description="제목", alias="ARTICLE_TITLE")
    CATEGORY_ID: str | None = Field(None, description="분류번호", alias="CATEGORY_ID")
    CATEGORY_NM: str | None = Field(None, description="구분", alias="CATEGORY_NM")
    CREATE_DT: str | None = Field(None, description="등록일", alias="CREATE_DT")

class Model_OOWY4R001216HX11494(BaseModel):
    """Response model for OOWY4R001216HX11494"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    PPSR_KIND: Union[str, int, float, None] = Field(None, description="제안자구분", alias="PPSR_KIND")
    PPSL_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PPSL_DT")
    ADCMIT_NM: Union[str, int, float, None] = Field(None, description="예비심사 위원회명", alias="ADCMIT_NM")
    ADCMIT_CMMT_DT: Union[str, int, float, None] = Field(None, description="예비심사 회부일", alias="ADCMIT_CMMT_DT")
    ADCMIT_PRSNT_DT: Union[str, int, float, None] = Field(None, description="예비심사 상정일", alias="ADCMIT_PRSNT_DT")
    ADCMIT_PROC_DT: Union[str, int, float, None] = Field(None, description="예비심사 의결일", alias="ADCMIT_PROC_DT")
    ADCMIT_PROC_RSLT: Union[str, int, float, None] = Field(None, description="예비심사 결과", alias="ADCMIT_PROC_RSLT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11494(BaseModel):
    """Request parameters for OOWY4R001216HX11494"""
    BILL_ID: str = Field(..., description="의안ID", alias="BILL_ID")

class Model_OXN4AR0009078I18280(BaseModel):
    """Response model for OXN4AR0009078I18280"""
    YR: Union[str, int, float, None] = Field(None, description="년도", alias="YR")
    SN: Union[str, int, float, None] = Field(None, description="일련번호", alias="SN")
    DEMD_RSON: Union[str, int, float, None] = Field(None, description="청구사항>청구내용", alias="DEMD_RSON")
    OPB_FOM_NM: Union[str, int, float, None] = Field(None, description="청구사항>공개형태", alias="OPB_FOM_NM")
    CHRG_DEPT_NM: Union[str, int, float, None] = Field(None, description="결정내용>담당부서", alias="CHRG_DEPT_NM")
    DCS_DIV: Union[str, int, float, None] = Field(None, description="결정내용>결정구분", alias="DCS_DIV")
    OPB_RSON: Union[str, int, float, None] = Field(None, description="결정내용>공개내용", alias="OPB_RSON")
    CLSD_RSON: Union[str, int, float, None] = Field(None, description="결정내용>비공개(부분공개) 내용 및 사유", alias="CLSD_RSON")
    DCS_NTC_DT: Union[str, int, float, None] = Field(None, description="결정내용>결정통지일자", alias="DCS_NTC_DT")
    OPB_DT: Union[str, int, float, None] = Field(None, description="처리사항>공개일자", alias="OPB_DT")
    OPB_MTH: Union[str, int, float, None] = Field(None, description="처리사항>공개방법", alias="OPB_MTH")

class Params_OXN4AR0009078I18280(BaseModel):
    """Request parameters for OXN4AR0009078I18280"""
    YR: str | None = Field(None, description="년도", alias="YR")
    SN: str | None = Field(None, description="일련번호", alias="SN")
    DEMD_RSON: str | None = Field(None, description="청구사항>청구내용", alias="DEMD_RSON")
    OPB_FOM_NM: str | None = Field(None, description="청구사항>공개형태", alias="OPB_FOM_NM")
    CHRG_DEPT_NM: str | None = Field(None, description="결정내용>담당부서", alias="CHRG_DEPT_NM")
    DCS_DIV: str | None = Field(None, description="결정내용>결정구분", alias="DCS_DIV")
    OPB_RSON: str | None = Field(None, description="결정내용>공개내용", alias="OPB_RSON")
    CLSD_RSON: str | None = Field(None, description="결정내용>비공개(부분공개) 내용 및 사유", alias="CLSD_RSON")
    OPB_MTH: str | None = Field(None, description="처리사항>공개방법", alias="OPB_MTH")

class Model_OOWY4R001216HX11522(BaseModel):
    """Response model for OOWY4R001216HX11522"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    FILE_CN: Union[str, int, float, None] = Field(None, description="파일설명", alias="FILE_CN")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11522(BaseModel):
    """Request parameters for OOWY4R001216HX11522"""
    CONF_ID: str | None = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: str | None = Field(None, description="대수", alias="ERACO")

class Model_OUSZ4M0011845C16071(BaseModel):
    """Response model for OUSZ4M0011845C16071"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="제목", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_OUSZ4M0011845C16071(BaseModel):
    """Request parameters for OUSZ4M0011845C16071"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="제목", alias="SUBJECT")

class Model_OM5S9O0009857U12121(BaseModel):
    """Response model for OM5S9O0009857U12121"""
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    AGE: Union[str, int, float, None] = Field(None, description="대수", alias="AGE")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NAME")
    PROPOSER: Union[str, int, float, None] = Field(None, description="제안자", alias="PROPOSER")
    PROPOSER_KIND: Union[str, int, float, None] = Field(None, description="제안자구분", alias="PROPOSER_KIND")
    PROPOSE_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PROPOSE_DT")
    PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="본회의심의결과", alias="PROC_RESULT_CD")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위", alias="CURR_COMMITTEE")
    COMMITTEE_DT: Union[str, int, float, None] = Field(None, description="소관위회부일", alias="COMMITTEE_DT")
    PROC_DT: Union[str, int, float, None] = Field(None, description="의결일", alias="PROC_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="의안상세정보_URL", alias="LINK_URL")
    LAW_SUBMIT_DT: Union[str, int, float, None] = Field(None, description="법사위회부일", alias="LAW_SUBMIT_DT")
    LAW_PRESENT_DT: Union[str, int, float, None] = Field(None, description="법사위상정일", alias="LAW_PRESENT_DT")
    LAW_PROC_DT: Union[str, int, float, None] = Field(None, description="법사위처리일", alias="LAW_PROC_DT")
    CMT_PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="소관위처리결과", alias="CMT_PROC_RESULT_CD")
    LAW_PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="법사위처리결과", alias="LAW_PROC_RESULT_CD")
    CMT_PRESENT_DT: Union[str, int, float, None] = Field(None, description="소관위상정일", alias="CMT_PRESENT_DT")
    CMT_PROC_DT: Union[str, int, float, None] = Field(None, description="소관위처리일", alias="CMT_PROC_DT")

class Params_OM5S9O0009857U12121(BaseModel):
    """Request parameters for OM5S9O0009857U12121"""
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    AGE: str = Field(..., description="대수", alias="AGE")
    BILL_NAME: str | None = Field(None, description="의안명", alias="BILL_NAME")
    PROPOSER: str | None = Field(None, description="제안자", alias="PROPOSER")
    PROPOSER_KIND: str | None = Field(None, description="제안자구분", alias="PROPOSER_KIND")
    PROC_RESULT_CD: str | None = Field(None, description="본회의심의결과", alias="PROC_RESULT_CD")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: str | None = Field(None, description="소관위", alias="CURR_COMMITTEE")

class Model_O8YX0U001110EM14308(BaseModel):
    """Response model for O8YX0U001110EM14308"""
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_O8YX0U001110EM14308(BaseModel):
    """Request parameters for O8YX0U001110EM14308"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: str | None = Field(None, description="등록일자", alias="INSERTDT")

class Model_OY3EE5000956Q913543(BaseModel):
    """Response model for OY3EE5000956Q913543"""
    ARTICLE_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="ARTICLE_TITLE")
    WRITER_NM: Union[str, int, float, None] = Field(None, description="작성자", alias="WRITER_NM")
    UPDATE_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="UPDATE_DT")

class Params_OY3EE5000956Q913543(BaseModel):
    """Request parameters for OY3EE5000956Q913543"""
    ARTICLE_TITLE: str | None = Field(None, description="제목", alias="ARTICLE_TITLE")
    WRITER_NM: str | None = Field(None, description="작성자", alias="WRITER_NM")
    UPDATE_DT: str | None = Field(None, description="작성일", alias="UPDATE_DT")

class Model_OOWY4R001216HX11428(BaseModel):
    """Response model for OOWY4R001216HX11428"""
    PBLM_TTL: Union[str, int, float, None] = Field(None, description="발간물 제목", alias="PBLM_TTL")
    PBL_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="PBL_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11428(BaseModel):
    """Request parameters for OOWY4R001216HX11428"""
    PBLM_TTL: str | None = Field(None, description="발간물 제목", alias="PBLM_TTL")

class Model_OMGXFT001182IV12099(BaseModel):
    """Response model for OMGXFT001182IV12099"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_OMGXFT001182IV12099(BaseModel):
    """Request parameters for OMGXFT001182IV12099"""
    REG_DATE: str | None = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_OOWY4R001216HX11489(BaseModel):
    """Response model for OOWY4R001216HX11489"""
    PTT_ID: Union[str, int, float, None] = Field(None, description="청원ID", alias="PTT_ID")
    PTT_NO: Union[str, int, float, None] = Field(None, description="청원번호", alias="PTT_NO")
    PTT_NM: Union[str, int, float, None] = Field(None, description="청원명", alias="PTT_NM")
    PTT_KIND: Union[str, int, float, None] = Field(None, description="청원종류", alias="PTT_KIND")
    PTTR_NM: Union[str, int, float, None] = Field(None, description="청원자명", alias="PTTR_NM")
    INTD_ASBLM_NM: Union[str, int, float, None] = Field(None, description="소개의원명", alias="INTD_ASBLM_NM")
    CITZN_AGM_CNT: Union[str, int, float, None] = Field(None, description="국민동의건수", alias="CITZN_AGM_CNT")
    RCP_DT: Union[str, int, float, None] = Field(None, description="접수일", alias="RCP_DT")
    JRCMIT_NM: Union[str, int, float, None] = Field(None, description="소관위원회명", alias="JRCMIT_NM")
    JRCMIT_CMMT_DT: Union[str, int, float, None] = Field(None, description="소관위원회 회부일", alias="JRCMIT_CMMT_DT")
    JRCMIT_PRSNT_DT: Union[str, int, float, None] = Field(None, description="소관위원회 상정일", alias="JRCMIT_PRSNT_DT")
    JRCMIT_PROC_DT: Union[str, int, float, None] = Field(None, description="소관위원회 처리일", alias="JRCMIT_PROC_DT")
    JRCMIT_PROC_RSLT: Union[str, int, float, None] = Field(None, description="소관위원회 처리결과", alias="JRCMIT_PROC_RSLT")
    RGS_PRSNT_DT: Union[str, int, float, None] = Field(None, description="본회의 심의 상정일", alias="RGS_PRSNT_DT")
    RGS_RSLN_DT: Union[str, int, float, None] = Field(None, description="본회의 심의 의결일", alias="RGS_RSLN_DT")
    RGS_CONF_NM: Union[str, int, float, None] = Field(None, description="본회의 심의 회의명", alias="RGS_CONF_NM")
    RGS_CONF_RSLT: Union[str, int, float, None] = Field(None, description="본회의 심의결과", alias="RGS_CONF_RSLT")
    GVRN_TRSF_DT: Union[str, int, float, None] = Field(None, description="정부 이송일", alias="GVRN_TRSF_DT")
    GVRN_OC_NM: Union[str, int, float, None] = Field(None, description="정부 부처명", alias="GVRN_OC_NM")
    GVRN_RSLT_DT: Union[str, int, float, None] = Field(None, description="정부처리결과 보고일", alias="GVRN_RSLT_DT")
    PROC_NTC_DT: Union[str, int, float, None] = Field(None, description="처리 통지일", alias="PROC_NTC_DT")
    ACHV_RATIO: Union[str, int, float, None] = Field(None, description="달성도", alias="ACHV_RATIO")

class Params_OOWY4R001216HX11489(BaseModel):
    """Request parameters for OOWY4R001216HX11489"""
    PTT_ID: str = Field(..., description="청원ID", alias="PTT_ID")

class Model_O71AP8001122ZZ10743(BaseModel):
    """Response model for O71AP8001122ZZ10743"""
    PRDC_YM_NM: Union[str, int, float, None] = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: Union[str, int, float, None] = Field(None, description="공개파일명", alias="OPB_FL_NM")
    INST_CD: Union[str, int, float, None] = Field(None, description="기관코드", alias="INST_CD")
    INST_NM: Union[str, int, float, None] = Field(None, description="기관명", alias="INST_NM")
    OPB_FL_PH: Union[str, int, float, None] = Field(None, description="공개파일경로", alias="OPB_FL_PH")
    FILE_ID: Union[str, int, float, None] = Field(None, description="첨부파일ID", alias="FILE_ID")

class Params_O71AP8001122ZZ10743(BaseModel):
    """Request parameters for O71AP8001122ZZ10743"""
    PRDC_YM_NM: str | None = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: str | None = Field(None, description="공개파일명", alias="OPB_FL_NM")

class Model_OFJHWN000881T019291(BaseModel):
    """Response model for OFJHWN000881T019291"""
    CTR_RDT: Union[str, int, float, None] = Field(None, description="계약일자", alias="CTR_RDT")
    CTR_NM: Union[str, int, float, None] = Field(None, description="계약건명", alias="CTR_NM")
    CTR_AMT: Union[str, int, float, None] = Field(None, description="계약금액", alias="CTR_AMT")
    CTR_OJ_NM: Union[str, int, float, None] = Field(None, description="계약상대자", alias="CTR_OJ_NM")
    CTR_MTH: Union[str, int, float, None] = Field(None, description="계약방법", alias="CTR_MTH")
    PRVCTRT_RSON: Union[str, int, float, None] = Field(None, description="수의계약사유", alias="PRVCTRT_RSON")

class Params_OFJHWN000881T019291(BaseModel):
    """Request parameters for OFJHWN000881T019291"""
    CTR_NM: str | None = Field(None, description="계약건명", alias="CTR_NM")
    CTR_OJ_NM: str | None = Field(None, description="계약상대자", alias="CTR_OJ_NM")
    CTR_MTH: str | None = Field(None, description="계약방법", alias="CTR_MTH")
    PRVCTRT_RSON: str | None = Field(None, description="수의계약사유", alias="PRVCTRT_RSON")

class Model_OR137O001023MZ19321(BaseModel):
    """Response model for OR137O001023MZ19321"""
    CONFER_NUM: Union[str, int, float, None] = Field(None, description="회의번호", alias="CONFER_NUM")
    TITLE: Union[str, int, float, None] = Field(None, description="회의명", alias="TITLE")
    CLASS_NAME: Union[str, int, float, None] = Field(None, description="회의종류명", alias="CLASS_NAME")
    DAE_NUM: Union[str, int, float, None] = Field(None, description="대수", alias="DAE_NUM")
    COMM_NAME: Union[str, int, float, None] = Field(None, description="위원회명", alias="COMM_NAME")
    VODCOMM_CODE: Union[str, int, float, None] = Field(None, description="영상회의록", alias="VODCOMM_CODE")
    CONF_DATE: Union[str, int, float, None] = Field(None, description="회의날짜", alias="CONF_DATE")
    SUB_NAME: Union[str, int, float, None] = Field(None, description="안건명", alias="SUB_NAME")
    VOD_LINK_URL: Union[str, int, float, None] = Field(None, description="영상회의록 링크", alias="VOD_LINK_URL")
    CONF_LINK_URL: Union[str, int, float, None] = Field(None, description="요약정보 팝업", alias="CONF_LINK_URL")
    PDF_LINK_URL: Union[str, int, float, None] = Field(None, description="PDF파일 링크", alias="PDF_LINK_URL")
    PDF_FILE_ID: Union[str, int, float, None] = Field(None, description="회의록", alias="PDF_FILE_ID")
    DEPT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="DEPT_CD")
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")

class Params_OR137O001023MZ19321(BaseModel):
    """Request parameters for OR137O001023MZ19321"""
    TITLE: str | None = Field(None, description="회의명", alias="TITLE")
    CLASS_NAME: str | None = Field(None, description="회의종류명", alias="CLASS_NAME")
    DAE_NUM: str = Field(..., description="대수", alias="DAE_NUM")
    COMM_NAME: str | None = Field(None, description="위원회명", alias="COMM_NAME")
    CONF_DATE: str = Field(..., description="회의날짜", alias="CONF_DATE")
    SUB_NAME: str | None = Field(None, description="안건명", alias="SUB_NAME")
    DEPT_CD: str | None = Field(None, description="위원회코드", alias="DEPT_CD")

class Model_O5IUE30009237O13905(BaseModel):
    """Response model for O5IUE30009237O13905"""
    RPT_NO: Union[str, int, float, None] = Field(None, description="다운로드", alias="RPT_NO")
    RPT_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="RPT_TITLE")
    STND_DT: Union[str, int, float, None] = Field(None, description="기준일자", alias="STND_DT")
    WRT_NM: Union[str, int, float, None] = Field(None, description="작성자", alias="WRT_NM")
    UNIT_CD: Union[str, int, float, None] = Field(None, description="대별코드", alias="UNIT_CD")
    UNIT_NM: Union[str, int, float, None] = Field(None, description="대", alias="UNIT_NM")
    FILE_ID: Union[str, int, float, None] = Field(None, description="파일ID", alias="FILE_ID")

class Params_O5IUE30009237O13905(BaseModel):
    """Request parameters for O5IUE30009237O13905"""
    RPT_TITLE: str | None = Field(None, description="제목", alias="RPT_TITLE")
    STND_DT: str | None = Field(None, description="기준일자", alias="STND_DT")
    WRT_NM: str | None = Field(None, description="작성자", alias="WRT_NM")
    UNIT_NM: str | None = Field(None, description="대", alias="UNIT_NM")

class Model_ORNDP7000993P115502(BaseModel):
    """Response model for ORNDP7000993P115502"""
    HG_NM: Union[str, int, float, None] = Field(None, description="의원이름(한글)", alias="HG_NM")
    HJ_NM: Union[str, int, float, None] = Field(None, description="의원이름(한자)", alias="HJ_NM")
    FRTO_DATE: Union[str, int, float, None] = Field(None, description="활동기간", alias="FRTO_DATE")
    PROFILE_SJ: Union[str, int, float, None] = Field(None, description="위원회 경력", alias="PROFILE_SJ")
    MONA_CD: Union[str, int, float, None] = Field(None, description="국회의원코드", alias="MONA_CD")
    PROFILE_UNIT_CD: Union[str, int, float, None] = Field(None, description="경력대수코드", alias="PROFILE_UNIT_CD")
    PROFILE_UNIT_NM: Union[str, int, float, None] = Field(None, description="경력대수", alias="PROFILE_UNIT_NM")

class Params_ORNDP7000993P115502(BaseModel):
    """Request parameters for ORNDP7000993P115502"""
    HG_NM: str | None = Field(None, description="의원이름(한글)", alias="HG_NM")
    PROFILE_SJ: str | None = Field(None, description="위원회 경력", alias="PROFILE_SJ")
    MONA_CD: str | None = Field(None, description="국회의원코드", alias="MONA_CD")
    PROFILE_UNIT_CD: str | None = Field(None, description="경력대수코드", alias="PROFILE_UNIT_CD")

class Model_OOG5NZ000976EC12112(BaseModel):
    """Response model for OOG5NZ000976EC12112"""
    V_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="V_TITLE")
    URL_LINK: Union[str, int, float, None] = Field(None, description="기사 URL", alias="URL_LINK")
    DATE_LASTMODIFIED: Union[str, int, float, None] = Field(None, description="최종수정일", alias="DATE_LASTMODIFIED")
    DATE_RELEASED: Union[str, int, float, None] = Field(None, description="기사작성일", alias="DATE_RELEASED")
    V_BODY: Union[str, int, float, None] = Field(None, description="기사내용", alias="V_BODY")

class Params_OOG5NZ000976EC12112(BaseModel):
    """Request parameters for OOG5NZ000976EC12112"""
    V_TITLE: str | None = Field(None, description="제목", alias="V_TITLE")

class Model_OXJ0OE001002XA11874(BaseModel):
    """Response model for OXJ0OE001002XA11874"""
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안 ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="법률안명", alias="BILL_NAME")
    AGE: Union[str, int, float, None] = Field(None, description="대", alias="AGE")
    PROPOSER_KIND_CD: Union[str, int, float, None] = Field(None, description="제안자구분", alias="PROPOSER_KIND_CD")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위원회", alias="CURR_COMMITTEE")
    NOTI_ED_DT: Union[str, int, float, None] = Field(None, description="게시종료일", alias="NOTI_ED_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크주소", alias="LINK_URL")
    PROPOSER: Union[str, int, float, None] = Field(None, description="제안자", alias="PROPOSER")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위ID", alias="CURR_COMMITTEE_ID")

class Params_OXJ0OE001002XA11874(BaseModel):
    """Request parameters for OXJ0OE001002XA11874"""
    BILL_ID: str | None = Field(None, description="의안 ID", alias="BILL_ID")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: str | None = Field(None, description="법률안명", alias="BILL_NAME")
    PROPOSER_KIND_CD: str | None = Field(None, description="제안자구분", alias="PROPOSER_KIND_CD")
    CURR_COMMITTEE: str | None = Field(None, description="소관위원회", alias="CURR_COMMITTEE")
    NOTI_ED_DT: str | None = Field(None, description="게시종료일", alias="NOTI_ED_DT")
    PROPOSER: str | None = Field(None, description="제안자", alias="PROPOSER")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위ID", alias="CURR_COMMITTEE_ID")

class Model_O4UTN7000934TV19125(BaseModel):
    """Response model for O4UTN7000934TV19125"""
    V_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="V_TITLE")
    URL_LINK: Union[str, int, float, None] = Field(None, description="기사 URL", alias="URL_LINK")
    DATE_LASTMODIFIED: Union[str, int, float, None] = Field(None, description="최종수정일", alias="DATE_LASTMODIFIED")
    DATE_RELEASED: Union[str, int, float, None] = Field(None, description="기사작성일", alias="DATE_RELEASED")
    V_BODY: Union[str, int, float, None] = Field(None, description="기사내용", alias="V_BODY")

class Params_O4UTN7000934TV19125(BaseModel):
    """Request parameters for O4UTN7000934TV19125"""
    V_TITLE: str | None = Field(None, description="제목", alias="V_TITLE")

class Model_OOWY4R001216HX11461(BaseModel):
    """Response model for OOWY4R001216HX11461"""
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    PPSR_KIND: Union[str, int, float, None] = Field(None, description="제안자구분", alias="PPSR_KIND")
    PPSR: Union[str, int, float, None] = Field(None, description="제안자", alias="PPSR")
    PPSL_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PPSL_DT")
    PPSL_SESS: Union[str, int, float, None] = Field(None, description="제안회기", alias="PPSL_SESS")
    JRCMIT_NM: Union[str, int, float, None] = Field(None, description="소관위원회명", alias="JRCMIT_NM")
    JRCMIT_CMMT_DT: Union[str, int, float, None] = Field(None, description="소관위원회 회부일", alias="JRCMIT_CMMT_DT")
    JRCMIT_PRSNT_DT: Union[str, int, float, None] = Field(None, description="소관위원회 상정일", alias="JRCMIT_PRSNT_DT")
    JRCMIT_PROC_DT: Union[str, int, float, None] = Field(None, description="소관위원회 처리일", alias="JRCMIT_PROC_DT")
    JRCMIT_PROC_RSLT: Union[str, int, float, None] = Field(None, description="소관위원회 처리결과", alias="JRCMIT_PROC_RSLT")
    LAW_CMMT_DT: Union[str, int, float, None] = Field(None, description="법사위 체계자구심사 회부일", alias="LAW_CMMT_DT")
    LAW_PRSNT_DT: Union[str, int, float, None] = Field(None, description="법사위 체계자구심사 상정일", alias="LAW_PRSNT_DT")
    LAW_PROC_DT: Union[str, int, float, None] = Field(None, description="법사위 체계자구심사 처리일", alias="LAW_PROC_DT")
    LAW_PROC_RSLT: Union[str, int, float, None] = Field(None, description="법사위 체계자구심사 처리결과", alias="LAW_PROC_RSLT")
    RGS_PRSNT_DT: Union[str, int, float, None] = Field(None, description="본회의 심의 상정일", alias="RGS_PRSNT_DT")
    RGS_RSLN_DT: Union[str, int, float, None] = Field(None, description="본회의 심의 의결일", alias="RGS_RSLN_DT")
    RGS_CONF_NM: Union[str, int, float, None] = Field(None, description="본회의 심의 회의명", alias="RGS_CONF_NM")
    RGS_CONF_RSLT: Union[str, int, float, None] = Field(None, description="본회의 심의결과", alias="RGS_CONF_RSLT")
    GVRN_TRSF_DT: Union[str, int, float, None] = Field(None, description="정부 이송일", alias="GVRN_TRSF_DT")
    PROM_LAW_NM: Union[str, int, float, None] = Field(None, description="공포 법률명", alias="PROM_LAW_NM")
    PROM_DT: Union[str, int, float, None] = Field(None, description="공포일", alias="PROM_DT")
    PROM_NO: Union[str, int, float, None] = Field(None, description="공포번호", alias="PROM_NO")

class Params_OOWY4R001216HX11461(BaseModel):
    """Request parameters for OOWY4R001216HX11461"""
    BILL_ID: str = Field(..., description="의안ID", alias="BILL_ID")

class Model_OI75DS001208ZW14781(BaseModel):
    """Response model for OI75DS001208ZW14781"""
    USE_START_DT: Union[str, int, float, None] = Field(None, description="일시", alias="USE_START_DT")
    USER_NM: Union[str, int, float, None] = Field(None, description="사용권자", alias="USER_NM")
    POLY_NM: Union[str, int, float, None] = Field(None, description="당명", alias="POLY_NM")
    CONT: Union[str, int, float, None] = Field(None, description="내용", alias="CONT")

class Params_OI75DS001208ZW14781(BaseModel):
    """Request parameters for OI75DS001208ZW14781"""
    pass

class Model_OCLLF20008904J19487(BaseModel):
    """Response model for OCLLF20008904J19487"""
    DIV_NM: Union[str, int, float, None] = Field(None, description="구분", alias="DIV_NM")
    BLDG_NM: Union[str, int, float, None] = Field(None, description="건물", alias="BLDG_NM")
    ARE: Union[str, int, float, None] = Field(None, description="면적(㎡)", alias="ARE")
    FLSP: Union[str, int, float, None] = Field(None, description="면적(평)", alias="FLSP")
    AMT: Union[str, int, float, None] = Field(None, description="금액", alias="AMT")
    YR: Union[str, int, float, None] = Field(None, description="년도", alias="YR")

class Params_OCLLF20008904J19487(BaseModel):
    """Request parameters for OCLLF20008904J19487"""
    DIV_NM: str | None = Field(None, description="구분", alias="DIV_NM")
    BLDG_NM: str | None = Field(None, description="건물", alias="BLDG_NM")
    YR: str | None = Field(None, description="년도", alias="YR")

class Model_OC9MRL000922KH15936(BaseModel):
    """Response model for OC9MRL000922KH15936"""
    YR: Union[str, int, float, None] = Field(None, description="년도", alias="YR")
    INST_NM: Union[str, int, float, None] = Field(None, description="기관명", alias="INST_NM")
    BDG_TAMT: Union[str, int, float, None] = Field(None, description="예산총액(천원)", alias="BDG_TAMT")

class Params_OC9MRL000922KH15936(BaseModel):
    """Request parameters for OC9MRL000922KH15936"""
    YR: str | None = Field(None, description="년도", alias="YR")
    INST_NM: str | None = Field(None, description="기관명", alias="INST_NM")

class Model_O6MZOL000912ZG15427(BaseModel):
    """Response model for O6MZOL000912ZG15427"""
    YR: Union[str, int, float, None] = Field(None, description="년도", alias="YR")
    SN: Union[str, int, float, None] = Field(None, description="일련번호", alias="SN")
    DEMD_RSON: Union[str, int, float, None] = Field(None, description="청구사항>청구내용", alias="DEMD_RSON")
    OPB_FOM_NM: Union[str, int, float, None] = Field(None, description="청구사항>공개형태", alias="OPB_FOM_NM")
    CHRG_DEPT_NM: Union[str, int, float, None] = Field(None, description="결정내용>담당부서", alias="CHRG_DEPT_NM")
    DCS_DIV: Union[str, int, float, None] = Field(None, description="결정내용>결정구분", alias="DCS_DIV")
    OPB_RSON: Union[str, int, float, None] = Field(None, description="결정내용>공개내용", alias="OPB_RSON")
    CLSD_RSON: Union[str, int, float, None] = Field(None, description="결정내용>비공개(부분공개) 내용 및 사유", alias="CLSD_RSON")
    DCS_NTC_DT: Union[str, int, float, None] = Field(None, description="결정내용>결정통지일자", alias="DCS_NTC_DT")
    OPB_DT: Union[str, int, float, None] = Field(None, description="처리사항>공개일자", alias="OPB_DT")
    OPB_MTH: Union[str, int, float, None] = Field(None, description="처리사항>공개방법", alias="OPB_MTH")

class Params_O6MZOL000912ZG15427(BaseModel):
    """Request parameters for O6MZOL000912ZG15427"""
    YR: str | None = Field(None, description="년도", alias="YR")
    SN: str | None = Field(None, description="일련번호", alias="SN")
    DEMD_RSON: str | None = Field(None, description="청구사항>청구내용", alias="DEMD_RSON")
    CHRG_DEPT_NM: str | None = Field(None, description="결정내용>담당부서", alias="CHRG_DEPT_NM")
    DCS_DIV: str | None = Field(None, description="결정내용>결정구분", alias="DCS_DIV")
    OPB_RSON: str | None = Field(None, description="결정내용>공개내용", alias="OPB_RSON")
    CLSD_RSON: str | None = Field(None, description="결정내용>비공개(부분공개) 내용 및 사유", alias="CLSD_RSON")
    DCS_NTC_DT: str | None = Field(None, description="결정내용>결정통지일자", alias="DCS_NTC_DT")

class Model_OU749A0011256511253(BaseModel):
    """Response model for OU749A0011256511253"""
    PRDC_YM_NM: Union[str, int, float, None] = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: Union[str, int, float, None] = Field(None, description="공개파일명", alias="OPB_FL_NM")
    INST_CD: Union[str, int, float, None] = Field(None, description="기관코드", alias="INST_CD")
    INST_NM: Union[str, int, float, None] = Field(None, description="기관명", alias="INST_NM")
    OPB_FL_PH: Union[str, int, float, None] = Field(None, description="공개파일경로", alias="OPB_FL_PH")
    FILE_ID: Union[str, int, float, None] = Field(None, description="첨부파일ID", alias="FILE_ID")

class Params_OU749A0011256511253(BaseModel):
    """Request parameters for OU749A0011256511253"""
    pass

class Model_OZHI8N000955DZ17739(BaseModel):
    """Response model for OZHI8N000955DZ17739"""
    ARTICLE_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="ARTICLE_TITLE")
    WRITER_NM: Union[str, int, float, None] = Field(None, description="작성자", alias="WRITER_NM")
    CATEGORY_NM: Union[str, int, float, None] = Field(None, description="구분2", alias="CATEGORY_NM")
    UPDATE_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="UPDATE_DT")
    MASTER_NM: Union[str, int, float, None] = Field(None, description="구분1", alias="MASTER_NM")
    LINK_URL: Union[str, int, float, None] = Field(None, description="상세보기URL", alias="LINK_URL")

class Params_OZHI8N000955DZ17739(BaseModel):
    """Request parameters for OZHI8N000955DZ17739"""
    ARTICLE_TITLE: str | None = Field(None, description="제목", alias="ARTICLE_TITLE")
    WRITER_NM: str | None = Field(None, description="작성자", alias="WRITER_NM")
    UPDATE_DT: str | None = Field(None, description="작성일", alias="UPDATE_DT")

class Model_OOWY4R001216HX11449(BaseModel):
    """Response model for OOWY4R001216HX11449"""
    CMIT_DIV_CD: Union[str, int, float, None] = Field(None, description="위원회구분코드", alias="CMIT_DIV_CD")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    CRMN_NM: Union[str, int, float, None] = Field(None, description="위원장명", alias="CRMN_NM")
    CMTM_PSNUM: Union[str, int, float, None] = Field(None, description="위원회 의원정수", alias="CMTM_PSNUM")
    CMTM_CNT: Union[str, int, float, None] = Field(None, description="현위원수", alias="CMTM_CNT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 URL", alias="LINK_URL")

class Params_OOWY4R001216HX11449(BaseModel):
    """Request parameters for OOWY4R001216HX11449"""
    CMIT_DIV_CD: str | None = Field(None, description="위원회구분코드", alias="CMIT_DIV_CD")
    CMIT_NM: str | None = Field(None, description="위원회명", alias="CMIT_NM")

class Model_O84OO9000939BC16536(BaseModel):
    """Response model for O84OO9000939BC16536"""
    TITLE_V: Union[str, int, float, None] = Field(None, description="제목", alias="TITLE_V")
    USE_YN: Union[str, int, float, None] = Field(None, description="상태", alias="USE_YN")
    REG_DT_D: Union[str, int, float, None] = Field(None, description="작성일", alias="REG_DT_D")
    DT: Union[str, int, float, None] = Field(None, description="기간", alias="DT")
    CONTENT_L: Union[str, int, float, None] = Field(None, description="내용", alias="CONTENT_L")
    DEPT_NM_V: Union[str, int, float, None] = Field(None, description="의원실", alias="DEPT_NM_V")

class Params_O84OO9000939BC16536(BaseModel):
    """Request parameters for O84OO9000939BC16536"""
    TITLE_V: str | None = Field(None, description="제목", alias="TITLE_V")
    USE_YN: str | None = Field(None, description="상태", alias="USE_YN")
    REG_DT_D: str | None = Field(None, description="작성일", alias="REG_DT_D")
    DT: str | None = Field(None, description="기간", alias="DT")
    CONTENT_L: str | None = Field(None, description="내용", alias="CONTENT_L")
    DEPT_NM_V: str | None = Field(None, description="의원실", alias="DEPT_NM_V")

class Model_OAUD9V000973QN17203(BaseModel):
    """Response model for OAUD9V000973QN17203"""
    V_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="V_TITLE")
    URL_LINK: Union[str, int, float, None] = Field(None, description="기사 URL", alias="URL_LINK")
    DATE_LASTMODIFIED: Union[str, int, float, None] = Field(None, description="최종수정일", alias="DATE_LASTMODIFIED")
    DATE_RELEASED: Union[str, int, float, None] = Field(None, description="기사작성일", alias="DATE_RELEASED")
    V_BODY: Union[str, int, float, None] = Field(None, description="기사내용", alias="V_BODY")

class Params_OAUD9V000973QN17203(BaseModel):
    """Request parameters for OAUD9V000973QN17203"""
    V_TITLE: str | None = Field(None, description="제목", alias="V_TITLE")

class Model_O6DY4U000931SN17960(BaseModel):
    """Response model for O6DY4U000931SN17960"""
    FSCL_YY: Union[str, int, float, None] = Field(None, description="회계년도", alias="FSCL_YY")
    EXE_M: Union[str, int, float, None] = Field(None, description="회계월", alias="EXE_M")
    FSCL_NM: Union[str, int, float, None] = Field(None, description="회계명", alias="FSCL_NM")
    IKWAN_NM: Union[str, int, float, None] = Field(None, description="수입관명", alias="IKWAN_NM")
    IHANG_NM: Union[str, int, float, None] = Field(None, description="수입항명", alias="IHANG_NM")
    IMOK_NM: Union[str, int, float, None] = Field(None, description="수입목명", alias="IMOK_NM")
    BDG_CAMT: Union[str, int, float, None] = Field(None, description="예산", alias="BDG_CAMT")
    RC_AMT: Union[str, int, float, None] = Field(None, description="수납본월금액", alias="RC_AMT")
    RC_AGGR_AMT: Union[str, int, float, None] = Field(None, description="수납누계금액", alias="RC_AGGR_AMT")

class Params_O6DY4U000931SN17960(BaseModel):
    """Request parameters for O6DY4U000931SN17960"""
    FSCL_YY: str | None = Field(None, description="회계년도", alias="FSCL_YY")
    EXE_M: str | None = Field(None, description="회계월", alias="EXE_M")
    FSCL_NM: str | None = Field(None, description="회계명", alias="FSCL_NM")
    IKWAN_NM: str | None = Field(None, description="수입관명", alias="IKWAN_NM")
    IHANG_NM: str | None = Field(None, description="수입항명", alias="IHANG_NM")
    IMOK_NM: str | None = Field(None, description="수입목명", alias="IMOK_NM")

class Model_ODI720001121MP14647(BaseModel):
    """Response model for ODI720001121MP14647"""
    PRDC_YM_NM: Union[str, int, float, None] = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: Union[str, int, float, None] = Field(None, description="공개파일명", alias="OPB_FL_NM")
    INST_CD: Union[str, int, float, None] = Field(None, description="기관코드", alias="INST_CD")
    INST_NM: Union[str, int, float, None] = Field(None, description="기관명", alias="INST_NM")
    CTGR_CD: Union[str, int, float, None] = Field(None, description="분류항목코드", alias="CTGR_CD")
    CTGR_NM: Union[str, int, float, None] = Field(None, description="분류항목", alias="CTGR_NM")
    OPB_FL_PH: Union[str, int, float, None] = Field(None, description="공개파일경로", alias="OPB_FL_PH")
    FILE_ID: Union[str, int, float, None] = Field(None, description="파일ID", alias="FILE_ID")

class Params_ODI720001121MP14647(BaseModel):
    """Request parameters for ODI720001121MP14647"""
    PRDC_YM: str | None = Field(None, description="생산년월", alias="PRDC_YM")
    OPB_FL_NM: str | None = Field(None, description="공개파일명", alias="OPB_FL_NM")

class Model_OR95JZ001114RS11521(BaseModel):
    """Response model for OR95JZ001114RS11521"""
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_OR95JZ001114RS11521(BaseModel):
    """Request parameters for OR95JZ001114RS11521"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: str | None = Field(None, description="등록일자", alias="INSERTDT")

class Model_OOWY4R001216HX11434(BaseModel):
    """Response model for OOWY4R001216HX11434"""
    CHM_DIV: Union[str, int, float, None] = Field(None, description="의장단구분 (의장, 부의장 구분)", alias="CHM_DIV")
    ARTC_TTL: Union[str, int, float, None] = Field(None, description="보도자료 제목", alias="ARTC_TTL")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일자", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11434(BaseModel):
    """Request parameters for OOWY4R001216HX11434"""
    CHM_DIV: str | None = Field(None, description="의장단구분 (의장, 부의장 구분)", alias="CHM_DIV")
    ARTC_TTL: str | None = Field(None, description="보도자료 제목", alias="ARTC_TTL")

class Model_O9KCDC000980U619570(BaseModel):
    """Response model for O9KCDC000980U619570"""
    V_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="V_TITLE")
    URL_LINK: Union[str, int, float, None] = Field(None, description="기사 URL", alias="URL_LINK")
    DATE_LASTMODIFIED: Union[str, int, float, None] = Field(None, description="최종수정일", alias="DATE_LASTMODIFIED")
    DATE_RELEASED: Union[str, int, float, None] = Field(None, description="기사작성일", alias="DATE_RELEASED")
    V_BODY: Union[str, int, float, None] = Field(None, description="기사내용", alias="V_BODY")

class Params_O9KCDC000980U619570(BaseModel):
    """Request parameters for O9KCDC000980U619570"""
    V_TITLE: str | None = Field(None, description="제목", alias="V_TITLE")
    URL_LINK: str | None = Field(None, description="기사 URL", alias="URL_LINK")

class Model_OK160H001152I912731(BaseModel):
    """Response model for OK160H001152I912731"""
    PRDC_YM_NM: Union[str, int, float, None] = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: Union[str, int, float, None] = Field(None, description="공개파일명", alias="OPB_FL_NM")
    INST_CD: Union[str, int, float, None] = Field(None, description="기관코드", alias="INST_CD")
    INST_NM: Union[str, int, float, None] = Field(None, description="기관명", alias="INST_NM")
    OPB_FL_PH: Union[str, int, float, None] = Field(None, description="공개파일경로", alias="OPB_FL_PH")
    CTGR_CD: Union[str, int, float, None] = Field(None, description="분류항목코드", alias="CTGR_CD")
    CTGR_NM: Union[str, int, float, None] = Field(None, description="분류항목", alias="CTGR_NM")
    FILE_ID: Union[str, int, float, None] = Field(None, description="파일ID", alias="FILE_ID")

class Params_OK160H001152I912731(BaseModel):
    """Request parameters for OK160H001152I912731"""
    PRDC_YM: str | None = Field(None, description="생산년월", alias="PRDC_YM")
    PRDC_YM_NM: str | None = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: str | None = Field(None, description="공개파일명", alias="OPB_FL_NM")

class Model_OU29AR0009890A11079(BaseModel):
    """Response model for OU29AR0009890A11079"""
    V_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="V_TITLE")
    URL_LINK: Union[str, int, float, None] = Field(None, description="기사 URL", alias="URL_LINK")
    DATE_LASTMODIFIED: Union[str, int, float, None] = Field(None, description="최종수정일", alias="DATE_LASTMODIFIED")
    DATE_RELEASED: Union[str, int, float, None] = Field(None, description="기사작성일", alias="DATE_RELEASED")
    V_BODY: Union[str, int, float, None] = Field(None, description="기사내용", alias="V_BODY")

class Params_OU29AR0009890A11079(BaseModel):
    """Request parameters for OU29AR0009890A11079"""
    V_TITLE: str | None = Field(None, description="제목", alias="V_TITLE")
    V_BODY: str | None = Field(None, description="기사내용", alias="V_BODY")

class Model_OVDKBQ000915NE11865(BaseModel):
    """Response model for OVDKBQ000915NE11865"""
    YR: Union[str, int, float, None] = Field(None, description="년도", alias="YR")
    INST_CD: Union[str, int, float, None] = Field(None, description="기관", alias="INST_CD")
    SN: Union[str, int, float, None] = Field(None, description="일련번호", alias="SN")
    IND_NM: Union[str, int, float, None] = Field(None, description="사건명", alias="IND_NM")
    APL_DT: Union[str, int, float, None] = Field(None, description="신청일", alias="APL_DT")
    ORDG_RSON: Union[str, int, float, None] = Field(None, description="주문내용", alias="ORDG_RSON")
    APL_MEAN: Union[str, int, float, None] = Field(None, description="신청취지", alias="APL_MEAN")
    DEAL_RSLT_MTH: Union[str, int, float, None] = Field(None, description="이유(처리결과요지)", alias="DEAL_RSLT_MTH")

class Params_OVDKBQ000915NE11865(BaseModel):
    """Request parameters for OVDKBQ000915NE11865"""
    YR: str | None = Field(None, description="년도", alias="YR")
    INST_CD: str | None = Field(None, description="기관", alias="INST_CD")
    SN: str | None = Field(None, description="일련번호", alias="SN")
    IND_NM: str | None = Field(None, description="사건명", alias="IND_NM")
    ORDG_RSON: str | None = Field(None, description="주문내용", alias="ORDG_RSON")
    APL_MEAN: str | None = Field(None, description="신청취지", alias="APL_MEAN")
    DEAL_RSLT_MTH: str | None = Field(None, description="이유(처리결과요지)", alias="DEAL_RSLT_MTH")

class Model_O87UNV000897E818234(BaseModel):
    """Response model for O87UNV000897E818234"""
    UNIT_CD: Union[str, int, float, None] = Field(None, description="대별코드", alias="UNIT_CD")
    PN: Union[str, int, float, None] = Field(None, description="성명", alias="PN")
    PURP_RSON: Union[str, int, float, None] = Field(None, description="목적사유", alias="PURP_RSON")
    SCH_DYS: Union[str, int, float, None] = Field(None, description="일정", alias="SCH_DYS")
    DSTN_NM: Union[str, int, float, None] = Field(None, description="목적지", alias="DSTN_NM")
    EXPNS_SUPPT_INST_NM: Union[str, int, float, None] = Field(None, description="경비지원기관", alias="EXPNS_SUPPT_INST_NM")
    REPORT_YN: Union[str, int, float, None] = Field(None, description="결과보고서", alias="REPORT_YN")
    UNIT_NM: Union[str, int, float, None] = Field(None, description="대", alias="UNIT_NM")

class Params_O87UNV000897E818234(BaseModel):
    """Request parameters for O87UNV000897E818234"""
    UNIT_CD: str | None = Field(None, description="대별코드", alias="UNIT_CD")
    PN: str | None = Field(None, description="성명", alias="PN")
    SCH_DYS: str | None = Field(None, description="일정", alias="SCH_DYS")
    DSTN_NM: str | None = Field(None, description="목적지", alias="DSTN_NM")
    UNIT_NM: str | None = Field(None, description="대", alias="UNIT_NM")

class Model_OHXILX000958DD14523(BaseModel):
    """Response model for OHXILX000958DD14523"""
    MEETING_DATE: Union[str, int, float, None] = Field(None, description="회의일자", alias="MEETING_DATE")
    MEETING_TIME: Union[str, int, float, None] = Field(None, description="시간", alias="MEETING_TIME")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DEGREE: Union[str, int, float, None] = Field(None, description="차수", alias="DEGREE")
    TITLE: Union[str, int, float, None] = Field(None, description="구분", alias="TITLE")
    COMMITTEE_NAME: Union[str, int, float, None] = Field(None, description="위원회 명", alias="COMMITTEE_NAME")
    LINK_URL2: Union[str, int, float, None] = Field(None, description="상세_URL", alias="LINK_URL2")
    UNIT_CD: Union[str, int, float, None] = Field(None, description="대수", alias="UNIT_CD")
    UNIT_NM: Union[str, int, float, None] = Field(None, description="대수", alias="UNIT_NM")
    HR_DEPT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="HR_DEPT_CD")
    ANGUN: Union[str, int, float, None] = Field(None, description="안건", alias="ANGUN")

class Params_OHXILX000958DD14523(BaseModel):
    """Request parameters for OHXILX000958DD14523"""
    MEETING_DATE: str | None = Field(None, description="회의일자", alias="MEETING_DATE")
    MEETING_TIME: str | None = Field(None, description="시간", alias="MEETING_TIME")
    SESS: str | None = Field(None, description="회기", alias="SESS")
    DEGREE: str | None = Field(None, description="차수", alias="DEGREE")
    TITLE: str | None = Field(None, description="구분", alias="TITLE")
    COMMITTEE_NAME: str | None = Field(None, description="위원회 명", alias="COMMITTEE_NAME")
    UNIT_CD: str = Field(..., description="대수", alias="UNIT_CD")
    HR_DEPT_CD: str | None = Field(None, description="위원회코드", alias="HR_DEPT_CD")

class Model_OOWY4R001216HX11506(BaseModel):
    """Response model for OOWY4R001216HX11506"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    CONF_KND: Union[str, int, float, None] = Field(None, description="회의종류", alias="CONF_KND")
    CMIT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="CMIT_CD")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운로드 URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11506(BaseModel):
    """Request parameters for OOWY4R001216HX11506"""
    ERACO: str = Field(..., description="대수", alias="ERACO")
    CMIT_CD: str | None = Field(None, description="위원회코드", alias="CMIT_CD")

class Model_O6P4Y5001146KI12348(BaseModel):
    """Response model for O6P4Y5001146KI12348"""
    DIV: Union[str, int, float, None] = Field(None, description="구분", alias="DIV")
    CHM_PN: Union[str, int, float, None] = Field(None, description="성명", alias="CHM_PN")
    CHM_APTM_YS: Union[str, int, float, None] = Field(None, description="재임기간", alias="CHM_APTM_YS")
    CHM_RMK: Union[str, int, float, None] = Field(None, description="비고", alias="CHM_RMK")
    UNIT_NM: Union[str, int, float, None] = Field(None, description="대", alias="UNIT_NM")

class Params_O6P4Y5001146KI12348(BaseModel):
    """Request parameters for O6P4Y5001146KI12348"""
    DIV: str | None = Field(None, description="구분", alias="DIV")
    CHM_PN: str | None = Field(None, description="성명", alias="CHM_PN")
    CHM_APTM_YS: str | None = Field(None, description="재임기간", alias="CHM_APTM_YS")
    UNIT_NM: str | None = Field(None, description="대", alias="UNIT_NM")

class Model_OBL7NF0011935G18076(BaseModel):
    """Response model for OBL7NF0011935G18076"""
    MONA_CD: Union[str, int, float, None] = Field(None, description="국회의원코드", alias="MONA_CD")
    HG_NM: Union[str, int, float, None] = Field(None, description="이름", alias="HG_NM")
    HJ_NM: Union[str, int, float, None] = Field(None, description="한자명", alias="HJ_NM")
    ENG_NM: Union[str, int, float, None] = Field(None, description="영문명칭", alias="ENG_NM")
    BTH_GBN_NM: Union[str, int, float, None] = Field(None, description="음/양력", alias="BTH_GBN_NM")
    BTH_DATE: Union[str, int, float, None] = Field(None, description="생년월일", alias="BTH_DATE")
    SEX_GBN_NM: Union[str, int, float, None] = Field(None, description="성별", alias="SEX_GBN_NM")
    REELE_GBN_NM: Union[str, int, float, None] = Field(None, description="재선", alias="REELE_GBN_NM")
    UNITS: Union[str, int, float, None] = Field(None, description="당선", alias="UNITS")
    UNIT_CD: Union[str, int, float, None] = Field(None, description="대별코드", alias="UNIT_CD")
    UNIT_NM: Union[str, int, float, None] = Field(None, description="대", alias="UNIT_NM")
    POLY_NM: Union[str, int, float, None] = Field(None, description="정당명", alias="POLY_NM")
    ORIG_NM: Union[str, int, float, None] = Field(None, description="선거구", alias="ORIG_NM")
    ELECT_GBN_NM: Union[str, int, float, None] = Field(None, description="선거구구분", alias="ELECT_GBN_NM")

class Params_OBL7NF0011935G18076(BaseModel):
    """Request parameters for OBL7NF0011935G18076"""
    MONA_CD: str | None = Field(None, description="국회의원코드", alias="MONA_CD")
    HG_NM: str | None = Field(None, description="이름", alias="HG_NM")
    SEX_GBN_NM: str | None = Field(None, description="성별", alias="SEX_GBN_NM")
    UNIT_CD: str = Field(..., description="대별코드", alias="UNIT_CD")
    POLY_NM: str | None = Field(None, description="정당명", alias="POLY_NM")
    ORIG_NM: str | None = Field(None, description="선거구", alias="ORIG_NM")

class Model_O610V6000952AV17729(BaseModel):
    """Response model for O610V6000952AV17729"""
    ARTICLE_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="ARTICLE_TITLE")
    DT: Union[str, int, float, None] = Field(None, description="일시", alias="DT")
    ETC_CHAR11: Union[str, int, float, None] = Field(None, description="장소", alias="ETC_CHAR11")
    ARTICLE_TEXT: Union[str, int, float, None] = Field(None, description="내용", alias="ARTICLE_TEXT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크주소", alias="LINK_URL")
    ATTACH_URL: Union[str, int, float, None] = Field(None, description="첨부파일URL", alias="ATTACH_URL")
    CATEGORY_NM: Union[str, int, float, None] = Field(None, description="구분명", alias="CATEGORY_NM")

class Params_O610V6000952AV17729(BaseModel):
    """Request parameters for O610V6000952AV17729"""
    ARTICLE_TITLE: str | None = Field(None, description="제목", alias="ARTICLE_TITLE")
    CATEGORY_NM: str | None = Field(None, description="구분명", alias="CATEGORY_NM")

class Model_OTUNFG0008834Q19898(BaseModel):
    """Response model for OTUNFG0008834Q19898"""
    YR: Union[str, int, float, None] = Field(None, description="연도", alias="YR")
    JBTP_NM: Union[str, int, float, None] = Field(None, description="직류", alias="JBTP_NM")
    ADPT_NOP: Union[str, int, float, None] = Field(None, description="채용인원", alias="ADPT_NOP")
    CMPT_RT: Union[str, int, float, None] = Field(None, description="경쟁률", alias="CMPT_RT")

class Params_OTUNFG0008834Q19898(BaseModel):
    """Request parameters for OTUNFG0008834Q19898"""
    YR: str | None = Field(None, description="연도", alias="YR")
    JBTP_NM: str | None = Field(None, description="직류", alias="JBTP_NM")

class Model_OK3DIS001059MR19626(BaseModel):
    """Response model for OK3DIS001059MR19626"""
    COMP_MAIN_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="COMP_MAIN_TITLE")
    REG_DATE: Union[str, int, float, None] = Field(None, description="등록일자", alias="REG_DATE")
    COMP_CONTENT: Union[str, int, float, None] = Field(None, description="내용", alias="COMP_CONTENT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="상세보기", alias="LINK_URL")

class Params_OK3DIS001059MR19626(BaseModel):
    """Request parameters for OK3DIS001059MR19626"""
    COMP_MAIN_TITLE: str | None = Field(None, description="제목", alias="COMP_MAIN_TITLE")
    COMP_CONTENT: str | None = Field(None, description="내용", alias="COMP_CONTENT")

class Model_O32948001073L213726(BaseModel):
    """Response model for O32948001073L213726"""
    AGE: Union[str, int, float, None] = Field(None, description="대수", alias="AGE")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NAME")
    BILL_KIND: Union[str, int, float, None] = Field(None, description="의안활동구분", alias="BILL_KIND")
    PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="의결결과", alias="PROC_RESULT_CD")
    VOTE_TCNT: Union[str, int, float, None] = Field(None, description="총투표수", alias="VOTE_TCNT")
    YES_TCNT: Union[str, int, float, None] = Field(None, description="찬성표수", alias="YES_TCNT")
    NO_TCNT: Union[str, int, float, None] = Field(None, description="반대수", alias="NO_TCNT")
    BLANK_TCNT: Union[str, int, float, None] = Field(None, description="기권수", alias="BLANK_TCNT")
    PROPOSE_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PROPOSE_DT")
    BDG_SUBMIT_DT: Union[str, int, float, None] = Field(None, description="예결위심사_회부일", alias="BDG_SUBMIT_DT")
    BDG_PRESENT_DT: Union[str, int, float, None] = Field(None, description="예결위심사_상정일", alias="BDG_PRESENT_DT")
    BDG_PROC_DT: Union[str, int, float, None] = Field(None, description="예결위심사_의결일", alias="BDG_PROC_DT")
    RGS_PRESENT_DT: Union[str, int, float, None] = Field(None, description="본회의심의_상정일", alias="RGS_PRESENT_DT")
    RGS_PROC_DT: Union[str, int, float, None] = Field(None, description="본회의심의_의결일", alias="RGS_PROC_DT")
    CURR_TRANS_DT: Union[str, int, float, None] = Field(None, description="정부이송일", alias="CURR_TRANS_DT")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위원회ID", alias="CURR_COMMITTEE_ID")
    COMMITTEE_NM: Union[str, int, float, None] = Field(None, description="소관위원회", alias="COMMITTEE_NM")

class Params_O32948001073L213726(BaseModel):
    """Request parameters for O32948001073L213726"""
    AGE: str = Field(..., description="대수", alias="AGE")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: str | None = Field(None, description="의안명", alias="BILL_NAME")
    PROC_RESULT_CD: str | None = Field(None, description="의결결과", alias="PROC_RESULT_CD")
    PROPOSE_DT: str | None = Field(None, description="제안일", alias="PROPOSE_DT")
    RGS_PROC_DT: str | None = Field(None, description="본회의심의_의결일", alias="RGS_PROC_DT")
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")

class Model_OOWY4R001216HX11491(BaseModel):
    """Response model for OOWY4R001216HX11491"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    RPT_TTL: Union[str, int, float, None] = Field(None, description="보고서제목명", alias="RPT_TTL")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    SBM_INST_NM: Union[str, int, float, None] = Field(None, description="제출기관명", alias="SBM_INST_NM")
    RCP_DT: Union[str, int, float, None] = Field(None, description="접수일", alias="RCP_DT")
    TRSF_DT: Union[str, int, float, None] = Field(None, description="이송일", alias="TRSF_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11491(BaseModel):
    """Request parameters for OOWY4R001216HX11491"""
    ERACO: str | None = Field(None, description="대수", alias="ERACO")
    CMIT_NM: str | None = Field(None, description="위원회명", alias="CMIT_NM")

class Model_OFZZ1G001167FC10024(BaseModel):
    """Response model for OFZZ1G001167FC10024"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_OFZZ1G001167FC10024(BaseModel):
    """Request parameters for OFZZ1G001167FC10024"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_OS18DL000970OU13480(BaseModel):
    """Response model for OS18DL000970OU13480"""
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    AGE: Union[str, int, float, None] = Field(None, description="대수", alias="AGE")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NAME")
    PROPOSER: Union[str, int, float, None] = Field(None, description="제안자", alias="PROPOSER")
    PROPOSER_KIND: Union[str, int, float, None] = Field(None, description="제안자구분", alias="PROPOSER_KIND")
    PROPOSE_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PROPOSE_DT")
    PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="본회의심의결과", alias="PROC_RESULT_CD")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위", alias="CURR_COMMITTEE")
    COMMITTEE_DT: Union[str, int, float, None] = Field(None, description="소관위회부일", alias="COMMITTEE_DT")
    PROC_DT: Union[str, int, float, None] = Field(None, description="의결일", alias="PROC_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="의안상세정보 URL", alias="LINK_URL")
    LAW_SUBMIT_DT: Union[str, int, float, None] = Field(None, description="법사위회부일", alias="LAW_SUBMIT_DT")
    LAW_PRESENT_DT: Union[str, int, float, None] = Field(None, description="법사위상정일", alias="LAW_PRESENT_DT")
    LAW_PROC_DT: Union[str, int, float, None] = Field(None, description="법사위처리일", alias="LAW_PROC_DT")
    CMT_PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="소관위처리결과", alias="CMT_PROC_RESULT_CD")
    LAW_PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="법사위처리결과", alias="LAW_PROC_RESULT_CD")
    CMT_PRESENT_DT: Union[str, int, float, None] = Field(None, description="소관위상정일", alias="CMT_PRESENT_DT")
    CMT_PROC_DT: Union[str, int, float, None] = Field(None, description="소관위처리일", alias="CMT_PROC_DT")

class Params_OS18DL000970OU13480(BaseModel):
    """Request parameters for OS18DL000970OU13480"""
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    AGE: str = Field(..., description="대수", alias="AGE")
    BILL_NAME: str | None = Field(None, description="의안명", alias="BILL_NAME")
    PROPOSER: str | None = Field(None, description="제안자", alias="PROPOSER")
    PROPOSER_KIND: str | None = Field(None, description="제안자구분", alias="PROPOSER_KIND")
    PROPOSE_DT: str | None = Field(None, description="제안일", alias="PROPOSE_DT")
    PROC_RESULT_CD: str | None = Field(None, description="본회의심의결과", alias="PROC_RESULT_CD")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: str | None = Field(None, description="소관위", alias="CURR_COMMITTEE")
    COMMITTEE_DT: str | None = Field(None, description="소관위회부일", alias="COMMITTEE_DT")
    PROC_DT: str | None = Field(None, description="의결일", alias="PROC_DT")

class Model_OB1YJN001063U411224(BaseModel):
    """Response model for OB1YJN001063U411224"""
    COMP_MAIN_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="COMP_MAIN_TITLE")
    REG_DATE: Union[str, int, float, None] = Field(None, description="등록일자", alias="REG_DATE")
    COMP_CONTENT: Union[str, int, float, None] = Field(None, description="내용", alias="COMP_CONTENT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="상세보기", alias="LINK_URL")

class Params_OB1YJN001063U411224(BaseModel):
    """Request parameters for OB1YJN001063U411224"""
    COMP_MAIN_TITLE: str | None = Field(None, description="제목", alias="COMP_MAIN_TITLE")
    COMP_CONTENT: str | None = Field(None, description="내용", alias="COMP_CONTENT")

class Model_OBV24T000974AX17644(BaseModel):
    """Response model for OBV24T000974AX17644"""
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    AGE: Union[str, int, float, None] = Field(None, description="대수", alias="AGE")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NAME")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위", alias="CURR_COMMITTEE")
    PROC_DT: Union[str, int, float, None] = Field(None, description="의결일", alias="PROC_DT")
    COMMITTEE_RESULT: Union[str, int, float, None] = Field(None, description="소관위처리결과", alias="COMMITTEE_RESULT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="상세정보_URL", alias="LINK_URL")
    COMMITTEE_PROC_DT: Union[str, int, float, None] = Field(None, description="소관위처리일", alias="COMMITTEE_PROC_DT")
    CMT_PRESENT_DT: Union[str, int, float, None] = Field(None, description="소관위상정일", alias="CMT_PRESENT_DT")
    LAW_SUBMIT_DT: Union[str, int, float, None] = Field(None, description="법사위회부일", alias="LAW_SUBMIT_DT")
    LAW_PRESENT_DT: Union[str, int, float, None] = Field(None, description="법사위상정일", alias="LAW_PRESENT_DT")
    LAW_PROC_DT: Union[str, int, float, None] = Field(None, description="법사위처리일", alias="LAW_PROC_DT")
    LAW_PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="법사위처리결과", alias="LAW_PROC_RESULT_CD")
    COMMITTEE_DT: Union[str, int, float, None] = Field(None, description="소관위회부일", alias="COMMITTEE_DT")

class Params_OBV24T000974AX17644(BaseModel):
    """Request parameters for OBV24T000974AX17644"""
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: str | None = Field(None, description="의안명", alias="BILL_NAME")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: str | None = Field(None, description="소관위", alias="CURR_COMMITTEE")
    COMMITTEE_RESULT: str | None = Field(None, description="소관위처리결과", alias="COMMITTEE_RESULT")

class Model_OOWY4R001216HX11490(BaseModel):
    """Response model for OOWY4R001216HX11490"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    PTT_ID: Union[str, int, float, None] = Field(None, description="청원ID", alias="PTT_ID")
    PTT_NO: Union[str, int, float, None] = Field(None, description="청원번호", alias="PTT_NO")
    PTT_NM: Union[str, int, float, None] = Field(None, description="청원명", alias="PTT_NM")
    PTT_KIND: Union[str, int, float, None] = Field(None, description="청원종류", alias="PTT_KIND")
    PTTR_NM: Union[str, int, float, None] = Field(None, description="청원자명", alias="PTTR_NM")
    INTD_ASBLM_NM: Union[str, int, float, None] = Field(None, description="소개의원명", alias="INTD_ASBLM_NM")
    CITZN_AGM_CNT: Union[str, int, float, None] = Field(None, description="국민동의건수", alias="CITZN_AGM_CNT")
    RCP_DT: Union[str, int, float, None] = Field(None, description="접수일", alias="RCP_DT")
    JRCMIT_NM: Union[str, int, float, None] = Field(None, description="소관위원회명", alias="JRCMIT_NM")
    JRCMIT_CMMT_DT: Union[str, int, float, None] = Field(None, description="소관위원회 회부일", alias="JRCMIT_CMMT_DT")
    JRCMIT_PRSNT_DT: Union[str, int, float, None] = Field(None, description="소관위원회 상정일", alias="JRCMIT_PRSNT_DT")
    JRCMIT_PROC_DT: Union[str, int, float, None] = Field(None, description="소관위원회 처리일", alias="JRCMIT_PROC_DT")
    JRCMIT_PROC_RSLT: Union[str, int, float, None] = Field(None, description="소관위원회 처리결과", alias="JRCMIT_PROC_RSLT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11490(BaseModel):
    """Request parameters for OOWY4R001216HX11490"""
    ERACO: str | None = Field(None, description="대수", alias="ERACO")

class Model_OHN9XR001210S614262(BaseModel):
    """Response model for OHN9XR001210S614262"""
    TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="TITLE")
    PLANNER: Union[str, int, float, None] = Field(None, description="기획자", alias="PLANNER")
    PANAL: Union[str, int, float, None] = Field(None, description="패널", alias="PANAL")
    REG_DTTM: Union[str, int, float, None] = Field(None, description="작성일", alias="REG_DTTM")
    OPEN_DTTM: Union[str, int, float, None] = Field(None, description="개최일", alias="OPEN_DTTM")
    DIV: Union[str, int, float, None] = Field(None, description="구분", alias="DIV")

class Params_OHN9XR001210S614262(BaseModel):
    """Request parameters for OHN9XR001210S614262"""
    pass

class Model_OBX2DO001030E516625(BaseModel):
    """Response model for OBX2DO001030E516625"""
    NUM: Union[str, int, float, None] = Field(None, description="게시물번호", alias="NUM")
    TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="TITLE")
    WRITE_DATE: Union[str, int, float, None] = Field(None, description="작성일", alias="WRITE_DATE")
    CONTENT: Union[str, int, float, None] = Field(None, description="내용", alias="CONTENT")
    CONTENT_URL: Union[str, int, float, None] = Field(None, description="상세내용URL", alias="CONTENT_URL")
    BBS_TITLE: Union[str, int, float, None] = Field(None, description="구분", alias="BBS_TITLE")

class Params_OBX2DO001030E516625(BaseModel):
    """Request parameters for OBX2DO001030E516625"""
    NUM: str | None = Field(None, description="게시물번호", alias="NUM")
    TITLE: str | None = Field(None, description="제목", alias="TITLE")
    WRITE_DATE: str | None = Field(None, description="작성일", alias="WRITE_DATE")
    CONTENT: str | None = Field(None, description="내용", alias="CONTENT")
    BBS_TITLE: str | None = Field(None, description="구분", alias="BBS_TITLE")

class Model_OZUY2X001061ON17910(BaseModel):
    """Response model for OZUY2X001061ON17910"""
    COMP_MAIN_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="COMP_MAIN_TITLE")
    REG_DATE: Union[str, int, float, None] = Field(None, description="등록일자", alias="REG_DATE")
    COMP_CONTENT: Union[str, int, float, None] = Field(None, description="내용", alias="COMP_CONTENT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="상세보기", alias="LINK_URL")

class Params_OZUY2X001061ON17910(BaseModel):
    """Request parameters for OZUY2X001061ON17910"""
    COMP_MAIN_TITLE: str | None = Field(None, description="제목", alias="COMP_MAIN_TITLE")
    REG_DATE: str = Field(..., description="등록일자", alias="REG_DATE")
    COMP_CONTENT: str | None = Field(None, description="내용", alias="COMP_CONTENT")

class Model_OAB4WY0009432M10546(BaseModel):
    """Response model for OAB4WY0009432M10546"""
    NOTICE_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="NOTICE_TITLE")
    DEPT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPT_NAME")
    WRITE_DATE: Union[str, int, float, None] = Field(None, description="작성일", alias="WRITE_DATE")
    CONTENT: Union[str, int, float, None] = Field(None, description="내용", alias="CONTENT")
    PDF_FILE_URL: Union[str, int, float, None] = Field(None, description="", alias="PDF_FILE_URL")
    ATTACH_FILE_URL: Union[str, int, float, None] = Field(None, description="첨부파일경로", alias="ATTACH_FILE_URL")

class Params_OAB4WY0009432M10546(BaseModel):
    """Request parameters for OAB4WY0009432M10546"""
    NOTICE_TITLE: str | None = Field(None, description="제목", alias="NOTICE_TITLE")
    DEPT_NAME: str | None = Field(None, description="부서명", alias="DEPT_NAME")
    WRITE_DATE: str | None = Field(None, description="작성일", alias="WRITE_DATE")
    CONTENT: str | None = Field(None, description="내용", alias="CONTENT")

class Model_OAJPOY0010182J19421(BaseModel):
    """Response model for OAJPOY0010182J19421"""
    HG_NM: Union[str, int, float, None] = Field(None, description="의원이름(한글)", alias="HG_NM")
    HJ_NM: Union[str, int, float, None] = Field(None, description="의원이름(한자)", alias="HJ_NM")
    FRTO_DATE: Union[str, int, float, None] = Field(None, description="활동기간", alias="FRTO_DATE")
    PROFILE_SJ: Union[str, int, float, None] = Field(None, description="의원이력", alias="PROFILE_SJ")
    MONA_CD: Union[str, int, float, None] = Field(None, description="국회의원코드", alias="MONA_CD")
    UNIT_CD: Union[str, int, float, None] = Field(None, description="대수코드", alias="UNIT_CD")
    UNIT_NM: Union[str, int, float, None] = Field(None, description="대수", alias="UNIT_NM")

class Params_OAJPOY0010182J19421(BaseModel):
    """Request parameters for OAJPOY0010182J19421"""
    HG_NM: str | None = Field(None, description="의원이름(한글)", alias="HG_NM")
    PROFILE_SJ: str | None = Field(None, description="의원이력", alias="PROFILE_SJ")
    MONA_CD: str | None = Field(None, description="국회의원코드", alias="MONA_CD")

class Model_OUK015001119KD17086(BaseModel):
    """Response model for OUK015001119KD17086"""
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_OUK015001119KD17086(BaseModel):
    """Request parameters for OUK015001119KD17086"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: str | None = Field(None, description="등록일자", alias="INSERTDT")

class Model_OOWY4R001216HX11472(BaseModel):
    """Response model for OOWY4R001216HX11472"""
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    RCP_CNT: Union[str, int, float, None] = Field(None, description="접수건수", alias="RCP_CNT")
    PROC_CNT: Union[str, int, float, None] = Field(None, description="처리건수", alias="PROC_CNT")
    RSVT_CNT: Union[str, int, float, None] = Field(None, description="보류건수", alias="RSVT_CNT")

class Params_OOWY4R001216HX11472(BaseModel):
    """Request parameters for OOWY4R001216HX11472"""
    ERACO: str = Field(..., description="대수", alias="ERACO")

class Model_OOWY4R001216HX11473(BaseModel):
    """Response model for OOWY4R001216HX11473"""
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    DRFBD_CNT: Union[str, int, float, None] = Field(None, description="예산안건수", alias="DRFBD_CNT")
    STL_CNT: Union[str, int, float, None] = Field(None, description="결산건수", alias="STL_CNT")
    LGSLB_ASBLM_PRPSR_CNT: Union[str, int, float, None] = Field(None, description="법률안의원발의건수", alias="LGSLB_ASBLM_PRPSR_CNT")
    LGSLB_GVRN_PRPSR_CNT: Union[str, int, float, None] = Field(None, description="법률안정부발의건수", alias="LGSLB_GVRN_PRPSR_CNT")
    LGSLB_SUM: Union[str, int, float, None] = Field(None, description="법률안합계", alias="LGSLB_SUM")
    AGMB_CNT: Union[str, int, float, None] = Field(None, description="동의안건수", alias="AGMB_CNT")
    RSLNB_GN_CNT: Union[str, int, float, None] = Field(None, description="결의안 일반 건수", alias="RSLNB_GN_CNT")
    RSLNB_ADIT_REQ_CNT: Union[str, int, float, None] = Field(None, description="결의안 감사요구 건수", alias="RSLNB_ADIT_REQ_CNT")
    RSLNB_SUBT: Union[str, int, float, None] = Field(None, description="결의안 소계", alias="RSLNB_SUBT")
    PRPSTB_CNT: Union[str, int, float, None] = Field(None, description="건의안건수", alias="PRPSTB_CNT")
    RULB_CNT: Union[str, int, float, None] = Field(None, description="규칙안 건수", alias="RULB_CNT")
    ELCTB_CNT: Union[str, int, float, None] = Field(None, description="선출안 건수", alias="ELCTB_CNT")
    IMPT_AGM_CNT: Union[str, int, float, None] = Field(None, description="중요동의 건수", alias="IMPT_AGM_CNT")
    CMTM_DSCP_CNT: Union[str, int, float, None] = Field(None, description="의원징계 건수", alias="CMTM_DSCP_CNT")
    CMTM_QLF_INSC_CNT: Union[str, int, float, None] = Field(None, description="의원자격심사 건수", alias="CMTM_QLF_INSC_CNT")
    CMIT_BY_SUM: Union[str, int, float, None] = Field(None, description="위원회별합계", alias="CMIT_BY_SUM")

class Params_OOWY4R001216HX11473(BaseModel):
    """Request parameters for OOWY4R001216HX11473"""
    ERACO: str = Field(..., description="대수", alias="ERACO")

class Model_OOWY4R001216HX11510(BaseModel):
    """Response model for OOWY4R001216HX11510"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    CONF_KND: Union[str, int, float, None] = Field(None, description="회의종류", alias="CONF_KND")
    CMIT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="CMIT_CD")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운로드 URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11510(BaseModel):
    """Request parameters for OOWY4R001216HX11510"""
    ERACO: str = Field(..., description="대수", alias="ERACO")
    CMIT_CD: str | None = Field(None, description="위원회코드", alias="CMIT_CD")

class Model_OOWY4R001216HX11460(BaseModel):
    """Response model for OOWY4R001216HX11460"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    PPSL_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PPSL_DT")
    PPSR_KIND: Union[str, int, float, None] = Field(None, description="제안자구분", alias="PPSR_KIND")
    PPSR_CN: Union[str, int, float, None] = Field(None, description="제안자설명", alias="PPSR_CN")
    PPSR_POLY_NM: Union[str, int, float, None] = Field(None, description="제안자정당명", alias="PPSR_POLY_NM")
    PPSR_NM: Union[str, int, float, None] = Field(None, description="제안자명", alias="PPSR_NM")
    PPSR_CH_NM: Union[str, int, float, None] = Field(None, description="제안자한자명", alias="PPSR_CH_NM")
    REP_DIV: Union[str, int, float, None] = Field(None, description="대표발의 구분", alias="REP_DIV")

class Params_OOWY4R001216HX11460(BaseModel):
    """Request parameters for OOWY4R001216HX11460"""
    BILL_ID: str = Field(..., description="의안ID", alias="BILL_ID")

class Model_OXJNQM001195IT17281(BaseModel):
    """Response model for OXJNQM001195IT17281"""
    PROFILE_CD: Union[str, int, float, None] = Field(None, description="구분코드", alias="PROFILE_CD")
    PROFILE_NM: Union[str, int, float, None] = Field(None, description="구분", alias="PROFILE_NM")
    HG_NM: Union[str, int, float, None] = Field(None, description="의원이름(한글)", alias="HG_NM")
    HJ_NM: Union[str, int, float, None] = Field(None, description="의원이름(한자)", alias="HJ_NM")
    FRTO_DATE: Union[str, int, float, None] = Field(None, description="활동기간", alias="FRTO_DATE")
    PROFILE_SJ: Union[str, int, float, None] = Field(None, description="위원회 경력", alias="PROFILE_SJ")
    MONA_CD: Union[str, int, float, None] = Field(None, description="국회의원코드", alias="MONA_CD")
    PROFILE_UNIT_CD: Union[str, int, float, None] = Field(None, description="경력대수코드", alias="PROFILE_UNIT_CD")
    PROFILE_UNIT_NM: Union[str, int, float, None] = Field(None, description="경력대수", alias="PROFILE_UNIT_NM")

class Params_OXJNQM001195IT17281(BaseModel):
    """Request parameters for OXJNQM001195IT17281"""
    HG_NM: str | None = Field(None, description="의원이름(한글)", alias="HG_NM")
    MONA_CD: str | None = Field(None, description="국회의원코드", alias="MONA_CD")
    PROFILE_UNIT_CD: str = Field(..., description="경력대수코드", alias="PROFILE_UNIT_CD")

class Model_OVDCJU001123OF14595(BaseModel):
    """Response model for OVDCJU001123OF14595"""
    PRDC_YM_NM: Union[str, int, float, None] = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: Union[str, int, float, None] = Field(None, description="공개파일명", alias="OPB_FL_NM")
    INST_CD: Union[str, int, float, None] = Field(None, description="기관코드", alias="INST_CD")
    INST_NM: Union[str, int, float, None] = Field(None, description="기관명", alias="INST_NM")
    OPB_FL_PH: Union[str, int, float, None] = Field(None, description="공개파일경로", alias="OPB_FL_PH")
    FILE_ID: Union[str, int, float, None] = Field(None, description="첨부파일ID", alias="FILE_ID")

class Params_OVDCJU001123OF14595(BaseModel):
    """Request parameters for OVDCJU001123OF14595"""
    PRDC_YM_NM: str | None = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: str | None = Field(None, description="공개파일명", alias="OPB_FL_NM")

class Model_O8D9RF000933S512258(BaseModel):
    """Response model for O8D9RF000933S512258"""
    FSCL_YY: Union[str, int, float, None] = Field(None, description="회계년도", alias="FSCL_YY")
    EXE_DATE: Union[str, int, float, None] = Field(None, description="집행일", alias="EXE_DATE")
    FSCL_NM: Union[str, int, float, None] = Field(None, description="회계명", alias="FSCL_NM")
    FLD_NM: Union[str, int, float, None] = Field(None, description="분야명", alias="FLD_NM")
    SECT_NM: Union[str, int, float, None] = Field(None, description="부문명", alias="SECT_NM")
    PGM_NM: Union[str, int, float, None] = Field(None, description="프로그램명", alias="PGM_NM")
    ACTV_NM: Union[str, int, float, None] = Field(None, description="단위사업명", alias="ACTV_NM")
    SACTV_NM: Union[str, int, float, None] = Field(None, description="세부사업명", alias="SACTV_NM")
    ANEXP_BDGAMT: Union[str, int, float, None] = Field(None, description="세출예산액", alias="ANEXP_BDGAMT")
    ANEXP_BDG_CAMT: Union[str, int, float, None] = Field(None, description="세출예산현액", alias="ANEXP_BDG_CAMT")
    EP_AMT: Union[str, int, float, None] = Field(None, description="지출금액", alias="EP_AMT")
    THISM_AGGR_EP_AMT: Union[str, int, float, None] = Field(None, description="연간누계지출금액", alias="THISM_AGGR_EP_AMT")
    THISM_AGGR_EP_NAMT: Union[str, int, float, None] = Field(None, description="당월누계지출순계금액", alias="THISM_AGGR_EP_NAMT")

class Params_O8D9RF000933S512258(BaseModel):
    """Request parameters for O8D9RF000933S512258"""
    FSCL_YY: str = Field(..., description="회계년도", alias="FSCL_YY")
    EXE_DATE: str | None = Field(None, description="집행일", alias="EXE_DATE")
    FSCL_NM: str | None = Field(None, description="회계명", alias="FSCL_NM")
    FLD_NM: str | None = Field(None, description="분야명", alias="FLD_NM")
    SECT_NM: str | None = Field(None, description="부문명", alias="SECT_NM")
    PGM_NM: str | None = Field(None, description="프로그램명", alias="PGM_NM")
    ACTV_NM: str | None = Field(None, description="단위사업명", alias="ACTV_NM")

class Model_OSKTB0000948E917810(BaseModel):
    """Response model for OSKTB0000948E917810"""
    ARTICLE_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="ARTICLE_TITLE")
    RE_DT: Union[str, int, float, None] = Field(None, description="관람예약", alias="RE_DT")
    DT: Union[str, int, float, None] = Field(None, description="일시", alias="DT")
    ETC_CHAR11: Union[str, int, float, None] = Field(None, description="장소", alias="ETC_CHAR11")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크주소", alias="LINK_URL")

class Params_OSKTB0000948E917810(BaseModel):
    """Request parameters for OSKTB0000948E917810"""
    ARTICLE_TITLE: str | None = Field(None, description="제목", alias="ARTICLE_TITLE")
    RE_DT: str | None = Field(None, description="관람예약", alias="RE_DT")
    DT: str | None = Field(None, description="일시", alias="DT")
    ETC_CHAR11: str | None = Field(None, description="장소", alias="ETC_CHAR11")

class Model_OCXHYA000859TX17626(BaseModel):
    """Response model for OCXHYA000859TX17626"""
    YEAR: Union[str, int, float, None] = Field(None, description="연도", alias="YEAR")
    DIV: Union[str, int, float, None] = Field(None, description="구분", alias="DIV")
    FLD: Union[str, int, float, None] = Field(None, description="분야", alias="FLD")
    GRP: Union[str, int, float, None] = Field(None, description="단체", alias="GRP")
    LAWMAKER: Union[str, int, float, None] = Field(None, description="대표의원", alias="LAWMAKER")
    PRZ_MONEY: Union[str, int, float, None] = Field(None, description="상금액", alias="PRZ_MONEY")

class Params_OCXHYA000859TX17626(BaseModel):
    """Request parameters for OCXHYA000859TX17626"""
    YEAR: str | None = Field(None, description="연도", alias="YEAR")
    DIV: str | None = Field(None, description="구분", alias="DIV")
    FLD: str | None = Field(None, description="분야", alias="FLD")
    GRP: str | None = Field(None, description="단체", alias="GRP")
    LAWMAKER: str | None = Field(None, description="대표의원", alias="LAWMAKER")

class Model_O7OLVS0011544713501(BaseModel):
    """Response model for O7OLVS0011544713501"""
    PRDC_YM_NM: Union[str, int, float, None] = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: Union[str, int, float, None] = Field(None, description="공개파일명", alias="OPB_FL_NM")
    INST_CD: Union[str, int, float, None] = Field(None, description="기관코드", alias="INST_CD")
    INST_NM: Union[str, int, float, None] = Field(None, description="기관명", alias="INST_NM")
    OPB_FL_PH: Union[str, int, float, None] = Field(None, description="공개파일경로", alias="OPB_FL_PH")
    CTGR_CD: Union[str, int, float, None] = Field(None, description="분류항목코드", alias="CTGR_CD")
    CTGR_NM: Union[str, int, float, None] = Field(None, description="분류항목", alias="CTGR_NM")
    FILE_ID: Union[str, int, float, None] = Field(None, description="파일ID", alias="FILE_ID")

class Params_O7OLVS0011544713501(BaseModel):
    """Request parameters for O7OLVS0011544713501"""
    PRDC_YM: str | None = Field(None, description="생산년월", alias="PRDC_YM")
    PRDC_YM_NM: str | None = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: str | None = Field(None, description="공개파일명", alias="OPB_FL_NM")

class Model_OJUGHY0009848Z17162(BaseModel):
    """Response model for OJUGHY0009848Z17162"""
    V_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="V_TITLE")
    URL_LINK: Union[str, int, float, None] = Field(None, description="기사 URL", alias="URL_LINK")
    DATE_LASTMODIFIED: Union[str, int, float, None] = Field(None, description="최종수정일", alias="DATE_LASTMODIFIED")
    DATE_RELEASED: Union[str, int, float, None] = Field(None, description="기사작성일", alias="DATE_RELEASED")
    V_BODY: Union[str, int, float, None] = Field(None, description="기사내용", alias="V_BODY")

class Params_OJUGHY0009848Z17162(BaseModel):
    """Request parameters for OJUGHY0009848Z17162"""
    V_TITLE: str | None = Field(None, description="제목", alias="V_TITLE")

class Model_O8OFB2000905T918825(BaseModel):
    """Response model for O8OFB2000905T918825"""
    YR: Union[str, int, float, None] = Field(None, description="년도", alias="YR")
    SN: Union[str, int, float, None] = Field(None, description="일련번호", alias="SN")
    DEMD_RSON: Union[str, int, float, None] = Field(None, description="청구사항>청구내용", alias="DEMD_RSON")
    OPB_FOM_NM: Union[str, int, float, None] = Field(None, description="청구사항>공개형태", alias="OPB_FOM_NM")
    CHRG_DEPT_NM: Union[str, int, float, None] = Field(None, description="결정내용>담당부서", alias="CHRG_DEPT_NM")
    DCS_DIV: Union[str, int, float, None] = Field(None, description="결정내용>결정구분", alias="DCS_DIV")
    OPB_RSON: Union[str, int, float, None] = Field(None, description="결정내용>공개내용", alias="OPB_RSON")
    CLSD_RSON: Union[str, int, float, None] = Field(None, description="결정내용>비공개(부분공개) 내용 및 사유", alias="CLSD_RSON")
    DCS_NTC_DT: Union[str, int, float, None] = Field(None, description="결정내용>결정통지일자", alias="DCS_NTC_DT")
    OPB_DT: Union[str, int, float, None] = Field(None, description="처리사항>공개일자", alias="OPB_DT")
    OPB_MTH: Union[str, int, float, None] = Field(None, description="처리사항>공개방법", alias="OPB_MTH")

class Params_O8OFB2000905T918825(BaseModel):
    """Request parameters for O8OFB2000905T918825"""
    YR: str | None = Field(None, description="년도", alias="YR")
    SN: str | None = Field(None, description="일련번호", alias="SN")
    DEMD_RSON: str | None = Field(None, description="청구사항>청구내용", alias="DEMD_RSON")
    OPB_FOM_NM: str | None = Field(None, description="청구사항>공개형태", alias="OPB_FOM_NM")
    CHRG_DEPT_NM: str | None = Field(None, description="결정내용>담당부서", alias="CHRG_DEPT_NM")
    DCS_DIV: str | None = Field(None, description="결정내용>결정구분", alias="DCS_DIV")
    OPB_RSON: str | None = Field(None, description="결정내용>공개내용", alias="OPB_RSON")
    CLSD_RSON: str | None = Field(None, description="결정내용>비공개(부분공개) 내용 및 사유", alias="CLSD_RSON")

class Model_OCFWMF000949MH18411(BaseModel):
    """Response model for OCFWMF000949MH18411"""
    ARTICLE_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="ARTICLE_TITLE")
    RE_DT: Union[str, int, float, None] = Field(None, description="관람예약", alias="RE_DT")
    DT: Union[str, int, float, None] = Field(None, description="일시", alias="DT")
    ETC_CHAR11: Union[str, int, float, None] = Field(None, description="장소", alias="ETC_CHAR11")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크주소", alias="LINK_URL")

class Params_OCFWMF000949MH18411(BaseModel):
    """Request parameters for OCFWMF000949MH18411"""
    ARTICLE_TITLE: str | None = Field(None, description="제목", alias="ARTICLE_TITLE")
    RE_DT: str | None = Field(None, description="관람예약", alias="RE_DT")
    DT: str | None = Field(None, description="일시", alias="DT")
    ETC_CHAR11: str | None = Field(None, description="장소", alias="ETC_CHAR11")

class Model_OOWY4R001216HX11441(BaseModel):
    """Response model for OOWY4R001216HX11441"""
    MTR_DIV: Union[str, int, float, None] = Field(None, description="발간자료구분", alias="MTR_DIV")
    MTR_TTL: Union[str, int, float, None] = Field(None, description="발간자료제목", alias="MTR_TTL")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11441(BaseModel):
    """Request parameters for OOWY4R001216HX11441"""
    MTR_DIV: str | None = Field(None, description="발간자료구분", alias="MTR_DIV")
    MTR_TTL: str | None = Field(None, description="발간자료제목", alias="MTR_TTL")

class Model_OC0RRQ000852J210654(BaseModel):
    """Response model for OC0RRQ000852J210654"""
    GUBUN: Union[str, int, float, None] = Field(None, description="구분", alias="GUBUN")
    YEAR: Union[str, int, float, None] = Field(None, description="연도", alias="YEAR")
    GROUP_CNT: Union[str, int, float, None] = Field(None, description="단체수(개)", alias="GROUP_CNT")

class Params_OC0RRQ000852J210654(BaseModel):
    """Request parameters for OC0RRQ000852J210654"""
    GUBUN: str | None = Field(None, description="구분", alias="GUBUN")
    YEAR: str | None = Field(None, description="연도", alias="YEAR")

class Model_O8WI650012155G10023(BaseModel):
    """Response model for O8WI650012155G10023"""
    CONFER_NUM: Union[str, int, float, None] = Field(None, description="회의번호", alias="CONFER_NUM")
    TITLE: Union[str, int, float, None] = Field(None, description="회의명", alias="TITLE")
    CLASS_NAME: Union[str, int, float, None] = Field(None, description="회의종류명", alias="CLASS_NAME")
    DAE_NUM: Union[str, int, float, None] = Field(None, description="대수", alias="DAE_NUM")
    CONF_DATE: Union[str, int, float, None] = Field(None, description="회의날짜", alias="CONF_DATE")
    SUB_NAME: Union[str, int, float, None] = Field(None, description="안건명", alias="SUB_NAME")
    VOD_LINK_URL: Union[str, int, float, None] = Field(None, description="영상회의록 링크", alias="VOD_LINK_URL")
    CONF_LINK_URL: Union[str, int, float, None] = Field(None, description="요약정보 팝업", alias="CONF_LINK_URL")
    PDF_LINK_URL: Union[str, int, float, None] = Field(None, description="PDF파일 링크", alias="PDF_LINK_URL")
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")

class Params_O8WI650012155G10023(BaseModel):
    """Request parameters for O8WI650012155G10023"""
    TITLE: str | None = Field(None, description="회의명", alias="TITLE")
    CLASS_NAME: str | None = Field(None, description="회의종류명", alias="CLASS_NAME")
    DAE_NUM: str = Field(..., description="대수", alias="DAE_NUM")
    CONF_DATE: str = Field(..., description="회의날짜", alias="CONF_DATE")
    SUB_NUM: str | None = Field(None, description="안건번호", alias="SUB_NUM")
    SUB_NAME: str | None = Field(None, description="안건명", alias="SUB_NAME")

class Model_OND1KZ0009677M13515(BaseModel):
    """Response model for OND1KZ0009677M13515"""
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    PROC_DT: Union[str, int, float, None] = Field(None, description="처리일", alias="PROC_DT")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NAME")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위", alias="CURR_COMMITTEE")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="표결결과", alias="PROC_RESULT_CD")
    BILL_KIND_CD: Union[str, int, float, None] = Field(None, description="의안종류", alias="BILL_KIND_CD")
    AGE: Union[str, int, float, None] = Field(None, description="대수", alias="AGE")
    MEMBER_TCNT: Union[str, int, float, None] = Field(None, description="재적의원", alias="MEMBER_TCNT")
    VOTE_TCNT: Union[str, int, float, None] = Field(None, description="총투표수", alias="VOTE_TCNT")
    YES_TCNT: Union[str, int, float, None] = Field(None, description="찬성", alias="YES_TCNT")
    NO_TCNT: Union[str, int, float, None] = Field(None, description="반대", alias="NO_TCNT")
    BLANK_TCNT: Union[str, int, float, None] = Field(None, description="기권", alias="BLANK_TCNT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="의안상세정보 URL", alias="LINK_URL")

class Params_OND1KZ0009677M13515(BaseModel):
    """Request parameters for OND1KZ0009677M13515"""
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: str | None = Field(None, description="의안명", alias="BILL_NAME")
    CURR_COMMITTEE: str | None = Field(None, description="소관위", alias="CURR_COMMITTEE")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    PROC_RESULT_CD: str | None = Field(None, description="표결결과", alias="PROC_RESULT_CD")
    BILL_KIND_CD: str | None = Field(None, description="의안종류", alias="BILL_KIND_CD")
    AGE: str = Field(..., description="대수", alias="AGE")

class Model_OOWY4R001216HX11443(BaseModel):
    """Response model for OOWY4R001216HX11443"""
    MTR_DIV: Union[str, int, float, None] = Field(None, description="발간자료구분", alias="MTR_DIV")
    MTR_TTL: Union[str, int, float, None] = Field(None, description="발간자료제목", alias="MTR_TTL")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11443(BaseModel):
    """Request parameters for OOWY4R001216HX11443"""
    MTR_DIV: str | None = Field(None, description="발간자료구분", alias="MTR_DIV")
    MTR_TTL: str | None = Field(None, description="발간자료제목", alias="MTR_TTL")

class Model_OQ50H1000962NX16376(BaseModel):
    """Response model for OQ50H1000962NX16376"""
    BILL_NO: Union[str, int, float, None] = Field(None, description="청원번호", alias="BILL_NO")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    AGE: Union[str, int, float, None] = Field(None, description="대", alias="AGE")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="청원명", alias="BILL_NAME")
    PROPOSER: Union[str, int, float, None] = Field(None, description="청원인", alias="PROPOSER")
    APPROVER: Union[str, int, float, None] = Field(None, description="소개의원", alias="APPROVER")
    PROPOSE_DT: Union[str, int, float, None] = Field(None, description="접수일자", alias="PROPOSE_DT")
    PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="의결결과", alias="PROC_RESULT_CD")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위", alias="CURR_COMMITTEE")
    COMMITTEE_DT: Union[str, int, float, None] = Field(None, description="위원회회부일", alias="COMMITTEE_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="상세보기URL", alias="LINK_URL")

class Params_OQ50H1000962NX16376(BaseModel):
    """Request parameters for OQ50H1000962NX16376"""
    BILL_NO: str | None = Field(None, description="청원번호", alias="BILL_NO")
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    AGE: str = Field(..., description="대", alias="AGE")
    BILL_NAME: str | None = Field(None, description="청원명", alias="BILL_NAME")
    PROPOSER: str | None = Field(None, description="청원인", alias="PROPOSER")
    APPROVER: str | None = Field(None, description="소개의원", alias="APPROVER")
    PROC_RESULT_CD: str | None = Field(None, description="의결결과", alias="PROC_RESULT_CD")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: str | None = Field(None, description="소관위", alias="CURR_COMMITTEE")

class Model_O8ZYOF001109VJ11181(BaseModel):
    """Response model for O8ZYOF001109VJ11181"""
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_O8ZYOF001109VJ11181(BaseModel):
    """Request parameters for O8ZYOF001109VJ11181"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: str | None = Field(None, description="등록일자", alias="INSERTDT")

class Model_OLFZV7001148O518934(BaseModel):
    """Response model for OLFZV7001148O518934"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    GCL_ELEC_DIV: Union[str, int, float, None] = Field(None, description="대별선거구분", alias="GCL_ELEC_DIV")
    ELEC_DE: Union[str, int, float, None] = Field(None, description="선거일", alias="ELEC_DE")
    ASBLM_PSNUM: Union[str, int, float, None] = Field(None, description="의원정수", alias="ASBLM_PSNUM")
    TERM_BG: Union[str, int, float, None] = Field(None, description="임기시작", alias="TERM_BG")
    TERM_ED: Union[str, int, float, None] = Field(None, description="임기종료", alias="TERM_ED")
    PROD: Union[str, int, float, None] = Field(None, description="기간", alias="PROD")
    RMK: Union[str, int, float, None] = Field(None, description="비고", alias="RMK")

class Params_OLFZV7001148O518934(BaseModel):
    """Request parameters for OLFZV7001148O518934"""
    ERACO: str | None = Field(None, description="대수", alias="ERACO")
    GCL_ELEC_DIV: str | None = Field(None, description="대별선거구분", alias="GCL_ELEC_DIV")

class Model_O4K6HM0012064I15889(BaseModel):
    """Response model for O4K6HM0012064I15889"""
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    AGE: Union[str, int, float, None] = Field(None, description="대", alias="AGE")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="의안명(한글)", alias="BILL_NAME")
    PROPOSER: Union[str, int, float, None] = Field(None, description="제안자", alias="PROPOSER")
    PROPOSER_KIND: Union[str, int, float, None] = Field(None, description="제안자구분", alias="PROPOSER_KIND")
    PROPOSE_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PROPOSE_DT")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위", alias="CURR_COMMITTEE")
    COMMITTEE_DT: Union[str, int, float, None] = Field(None, description="소관위회부일", alias="COMMITTEE_DT")
    COMMITTEE_PROC_DT: Union[str, int, float, None] = Field(None, description="위원회심사_처리일", alias="COMMITTEE_PROC_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="의안상세정보_URL", alias="LINK_URL")
    RST_PROPOSER: Union[str, int, float, None] = Field(None, description="대표발의자", alias="RST_PROPOSER")
    LAW_PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="법사위처리결과", alias="LAW_PROC_RESULT_CD")
    LAW_PROC_DT: Union[str, int, float, None] = Field(None, description="법사위처리일", alias="LAW_PROC_DT")
    LAW_PRESENT_DT: Union[str, int, float, None] = Field(None, description="법사위상정일", alias="LAW_PRESENT_DT")
    LAW_SUBMIT_DT: Union[str, int, float, None] = Field(None, description="법사위회부일", alias="LAW_SUBMIT_DT")
    CMT_PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="소관위처리결과", alias="CMT_PROC_RESULT_CD")
    CMT_PROC_DT: Union[str, int, float, None] = Field(None, description="소관위처리일", alias="CMT_PROC_DT")
    CMT_PRESENT_DT: Union[str, int, float, None] = Field(None, description="소관위상정일", alias="CMT_PRESENT_DT")
    RST_MONA_CD: Union[str, int, float, None] = Field(None, description="대표발의자코드", alias="RST_MONA_CD")
    PROC_RESULT_CD: Union[str, int, float, None] = Field(None, description="본회의심의결과", alias="PROC_RESULT_CD")
    PROC_DT: Union[str, int, float, None] = Field(None, description="의결일", alias="PROC_DT")

class Params_O4K6HM0012064I15889(BaseModel):
    """Request parameters for O4K6HM0012064I15889"""
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    AGE: str = Field(..., description="대", alias="AGE")
    BILL_NAME: str | None = Field(None, description="의안명(한글)", alias="BILL_NAME")
    PROPOSER: str | None = Field(None, description="제안자", alias="PROPOSER")
    PROPOSER_KIND: str | None = Field(None, description="제안자구분", alias="PROPOSER_KIND")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    CURR_COMMITTEE: str | None = Field(None, description="소관위", alias="CURR_COMMITTEE")
    PROC_DT: str | None = Field(None, description="의결일", alias="PROC_DT")
    PROC_RESULT_CD: str | None = Field(None, description="본회의심의결과", alias="PROC_RESULT_CD")
    BILL_ID_REF: str | None = Field(None, description="참조의안코드", alias="BILL_ID_REF")

class Model_ORRHLL000916DN12489(BaseModel):
    """Response model for ORRHLL000916DN12489"""
    YR: Union[str, int, float, None] = Field(None, description="년도", alias="YR")
    INST_CD: Union[str, int, float, None] = Field(None, description="기관", alias="INST_CD")
    SN: Union[str, int, float, None] = Field(None, description="일련번호", alias="SN")
    IND_NM: Union[str, int, float, None] = Field(None, description="사건명", alias="IND_NM")
    RSLN_DT: Union[str, int, float, None] = Field(None, description="의결(재결)일", alias="RSLN_DT")
    OJ_DEMD_PN: Union[str, int, float, None] = Field(None, description="피청구인", alias="OJ_DEMD_PN")
    ORDG_RSON: Union[str, int, float, None] = Field(None, description="주문내용", alias="ORDG_RSON")
    DEMD_MEAN: Union[str, int, float, None] = Field(None, description="청구취지", alias="DEMD_MEAN")
    JUD_RSLT_MTH: Union[str, int, float, None] = Field(None, description="이유(심판결과요지)", alias="JUD_RSLT_MTH")

class Params_ORRHLL000916DN12489(BaseModel):
    """Request parameters for ORRHLL000916DN12489"""
    YR: str | None = Field(None, description="년도", alias="YR")
    INST_CD: str | None = Field(None, description="기관", alias="INST_CD")
    SN: str | None = Field(None, description="일련번호", alias="SN")
    IND_NM: str | None = Field(None, description="사건명", alias="IND_NM")
    RSLN_DT: str | None = Field(None, description="의결(재결)일", alias="RSLN_DT")
    OJ_DEMD_PN: str | None = Field(None, description="피청구인", alias="OJ_DEMD_PN")
    ORDG_RSON: str | None = Field(None, description="주문내용", alias="ORDG_RSON")
    DEMD_MEAN: str | None = Field(None, description="청구취지", alias="DEMD_MEAN")
    JUD_RSLT_MTH: str | None = Field(None, description="이유(심판결과요지)", alias="JUD_RSLT_MTH")

class Model_O4W19G001189TV11044(BaseModel):
    """Response model for O4W19G001189TV11044"""
    APPOINT_GRADE: Union[str, int, float, None] = Field(None, description="직위정보", alias="APPOINT_GRADE")
    APPOINT_NAME: Union[str, int, float, None] = Field(None, description="후보자명", alias="APPOINT_NAME")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NAME")
    PROPOSE_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PROPOSE_DT")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위원회", alias="CURR_COMMITTEE")
    SUBMIT_DT: Union[str, int, float, None] = Field(None, description="소관위 회부일", alias="SUBMIT_DT")
    PRESENT_DT: Union[str, int, float, None] = Field(None, description="소관위상정일", alias="PRESENT_DT")
    PROC_DT: Union[str, int, float, None] = Field(None, description="소관위처리일", alias="PROC_DT")
    PROC_RESULT: Union[str, int, float, None] = Field(None, description="처리결과", alias="PROC_RESULT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="바로가기URL", alias="LINK_URL")
    MP_BOOK_URL: Union[str, int, float, None] = Field(None, description="청문회실시계획서", alias="MP_BOOK_URL")
    AGE: Union[str, int, float, None] = Field(None, description="대수", alias="AGE")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위원회ID", alias="CURR_COMMITTEE_ID")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")

class Params_O4W19G001189TV11044(BaseModel):
    """Request parameters for O4W19G001189TV11044"""
    APPOINT_GRADE: str | None = Field(None, description="직위정보", alias="APPOINT_GRADE")
    APPOINT_NAME: str | None = Field(None, description="후보자명", alias="APPOINT_NAME")
    BILL_NAME: str | None = Field(None, description="의안명", alias="BILL_NAME")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    AGE: str | None = Field(None, description="대수", alias="AGE")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위원회ID", alias="CURR_COMMITTEE_ID")
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")

class Model_OOWY4R001216HX11430(BaseModel):
    """Response model for OOWY4R001216HX11430"""
    PBLM_TTL: Union[str, int, float, None] = Field(None, description="발간물 제목", alias="PBLM_TTL")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11430(BaseModel):
    """Request parameters for OOWY4R001216HX11430"""
    PBLM_TTL: str | None = Field(None, description="발간물 제목", alias="PBLM_TTL")

class Model_OOWY4R001216HX11447(BaseModel):
    """Response model for OOWY4R001216HX11447"""
    NAAS_EN_NM: Union[str, int, float, None] = Field(None, description="국회의원 영문명", alias="NAAS_EN_NM")
    NTR_DIV: Union[str, int, float, None] = Field(None, description="성별", alias="NTR_DIV")
    BTH_GBN_NM: Union[str, int, float, None] = Field(None, description="생일구분코드", alias="BTH_GBN_NM")
    BIRDY_DT: Union[str, int, float, None] = Field(None, description="생일일자", alias="BIRDY_DT")
    PLPT_NM: Union[str, int, float, None] = Field(None, description="정당명", alias="PLPT_NM")
    ELECD_NM: Union[str, int, float, None] = Field(None, description="선거구명", alias="ELECD_NM")
    ELECD_DIV_NM: Union[str, int, float, None] = Field(None, description="선거구구분명", alias="ELECD_DIV_NM")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    CMIT_DTY_NM: Union[str, int, float, None] = Field(None, description="위원회 직책명", alias="CMIT_DTY_NM")
    BLNG_CMIT_NM: Union[str, int, float, None] = Field(None, description="소속위원회명", alias="BLNG_CMIT_NM")
    RLCT_DIV_NM: Union[str, int, float, None] = Field(None, description="재선구분명", alias="RLCT_DIV_NM")
    GTELT_TMS: Union[str, int, float, None] = Field(None, description="당선횟수", alias="GTELT_TMS")
    NAAS_TEL_NO: Union[str, int, float, None] = Field(None, description="국회의원전화번호", alias="NAAS_TEL_NO")
    NAAS_EMAIL_ADDR: Union[str, int, float, None] = Field(None, description="국회의원이메일주소", alias="NAAS_EMAIL_ADDR")
    NAAS_HP_URL: Union[str, int, float, None] = Field(None, description="국회의원홈페이지URL", alias="NAAS_HP_URL")

class Params_OOWY4R001216HX11447(BaseModel):
    """Request parameters for OOWY4R001216HX11447"""
    NAAS_EN_NM: str | None = Field(None, description="국회의원 영문명", alias="NAAS_EN_NM")
    NAAS_CD: str | None = Field(None, description="국회의원 코드", alias="NAAS_CD")

class Model_OEEG26001115LX11448(BaseModel):
    """Response model for OEEG26001115LX11448"""
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_OEEG26001115LX11448(BaseModel):
    """Request parameters for OEEG26001115LX11448"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: str | None = Field(None, description="등록일자", alias="INSERTDT")

class Model_OZY6M30010164K11655(BaseModel):
    """Response model for OZY6M30010164K11655"""
    TAKING_DATE: Union[str, int, float, None] = Field(None, description="회견일", alias="TAKING_DATE")
    OPEN_TIME: Union[str, int, float, None] = Field(None, description="회견시각", alias="OPEN_TIME")
    TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="TITLE")
    PERSON: Union[str, int, float, None] = Field(None, description="발언자", alias="PERSON")
    REC_TIME: Union[str, int, float, None] = Field(None, description="재생시간", alias="REC_TIME")
    LINK_URL: Union[str, int, float, None] = Field(None, description="영상 바로보기", alias="LINK_URL")

class Params_OZY6M30010164K11655(BaseModel):
    """Request parameters for OZY6M30010164K11655"""
    TAKING_DATE: str = Field(..., description="회견일", alias="TAKING_DATE")
    TITLE: str | None = Field(None, description="제목", alias="TITLE")
    PERSON: str | None = Field(None, description="발언자", alias="PERSON")

class Model_ORPY580008959U11813(BaseModel):
    """Response model for ORPY580008959U11813"""
    YR: Union[str, int, float, None] = Field(None, description="년도", alias="YR")
    BZ_NM: Union[str, int, float, None] = Field(None, description="사업명", alias="BZ_NM")
    BDG_TAMT: Union[str, int, float, None] = Field(None, description="예산총액(원)", alias="BDG_TAMT")

class Params_ORPY580008959U11813(BaseModel):
    """Request parameters for ORPY580008959U11813"""
    YR: str | None = Field(None, description="년도", alias="YR")
    BZ_NM: str | None = Field(None, description="사업명", alias="BZ_NM")

class Model_O5UDG0001111CI11346(BaseModel):
    """Response model for O5UDG0001111CI11346"""
    PDFFILEURL: Union[str, int, float, None] = Field(None, description="PDF파일URL", alias="PDFFILEURL")
    VIEWERURL: Union[str, int, float, None] = Field(None, description="뷰어URL", alias="VIEWERURL")
    BOOKNM: Union[str, int, float, None] = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: Union[str, int, float, None] = Field(None, description="등록일자", alias="INSERTDT")

class Params_O5UDG0001111CI11346(BaseModel):
    """Request parameters for O5UDG0001111CI11346"""
    BOOKNM: str | None = Field(None, description="자료명", alias="BOOKNM")
    INSERTDT: str | None = Field(None, description="등록일자", alias="INSERTDT")

class Model_OAIEX00008855613861(BaseModel):
    """Response model for OAIEX00008855613861"""
    YR: Union[str, int, float, None] = Field(None, description="연도", alias="YR")
    JBTP_NM: Union[str, int, float, None] = Field(None, description="직류", alias="JBTP_NM")
    ADPT_NOP: Union[str, int, float, None] = Field(None, description="채용인원", alias="ADPT_NOP")
    CMPT_RT: Union[str, int, float, None] = Field(None, description="경쟁률", alias="CMPT_RT")

class Params_OAIEX00008855613861(BaseModel):
    """Request parameters for OAIEX00008855613861"""
    YR: str | None = Field(None, description="연도", alias="YR")
    JBTP_NM: str | None = Field(None, description="직류", alias="JBTP_NM")

class Model_OOWY4R001216HX11518(BaseModel):
    """Response model for OOWY4R001216HX11518"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    CONF_KND: Union[str, int, float, None] = Field(None, description="회의종류", alias="CONF_KND")
    CMIT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="CMIT_CD")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운로드 URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11518(BaseModel):
    """Request parameters for OOWY4R001216HX11518"""
    ERACO: str = Field(..., description="대수", alias="ERACO")
    CMIT_CD: str | None = Field(None, description="위원회코드", alias="CMIT_CD")

class Model_OOWY4R001216HX11482(BaseModel):
    """Response model for OOWY4R001216HX11482"""
    CITZN_AGM_CNT: Union[str, int, float, None] = Field(None, description="국민동의건수", alias="CITZN_AGM_CNT")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")
    INTD_ASBLM_NM: Union[str, int, float, None] = Field(None, description="소개의원명", alias="INTD_ASBLM_NM")
    RCP_DT: Union[str, int, float, None] = Field(None, description="접수일", alias="RCP_DT")
    PTT_ID: Union[str, int, float, None] = Field(None, description="청원ID", alias="PTT_ID")
    PTT_NM: Union[str, int, float, None] = Field(None, description="청원명", alias="PTT_NM")
    PTT_NO: Union[str, int, float, None] = Field(None, description="청원번호", alias="PTT_NO")
    PTTR_NM: Union[str, int, float, None] = Field(None, description="청원자명", alias="PTTR_NM")
    PTT_KIND: Union[str, int, float, None] = Field(None, description="청원종류", alias="PTT_KIND")

class Params_OOWY4R001216HX11482(BaseModel):
    """Request parameters for OOWY4R001216HX11482"""
    ERACO: str = Field(..., description="대수", alias="ERACO")

class Model_OTL4B3000889YI11365(BaseModel):
    """Response model for OTL4B3000889YI11365"""
    ARE: Union[str, int, float, None] = Field(None, description="수량", alias="ARE")
    AMT: Union[str, int, float, None] = Field(None, description="금액(원)", alias="AMT")
    YR: Union[str, int, float, None] = Field(None, description="년도", alias="YR")
    DIV_NM: Union[str, int, float, None] = Field(None, description="구분", alias="DIV_NM")

class Params_OTL4B3000889YI11365(BaseModel):
    """Request parameters for OTL4B3000889YI11365"""
    DIV_NM: str | None = Field(None, description="구분", alias="DIV_NM")
    YR: str | None = Field(None, description="년도", alias="YR")

class Model_O0IS020011724J12768(BaseModel):
    """Response model for O0IS020011724J12768"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_O0IS020011724J12768(BaseModel):
    """Request parameters for O0IS020011724J12768"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_OOWY4R001216HX11500(BaseModel):
    """Response model for OOWY4R001216HX11500"""
    MTR_DIV: Union[str, int, float, None] = Field(None, description="발간자료구분", alias="MTR_DIV")
    MTR_TTL: Union[str, int, float, None] = Field(None, description="발간자료제목", alias="MTR_TTL")
    WRT_DEPT: Union[str, int, float, None] = Field(None, description="작성부서", alias="WRT_DEPT")
    WRT_DT: Union[str, int, float, None] = Field(None, description="작성일", alias="WRT_DT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")

class Params_OOWY4R001216HX11500(BaseModel):
    """Request parameters for OOWY4R001216HX11500"""
    MTR_DIV: str | None = Field(None, description="발간자료구분", alias="MTR_DIV")
    MTR_TTL: str | None = Field(None, description="발간자료제목", alias="MTR_TTL")

class Model_O6JXFI0011292O12073(BaseModel):
    """Response model for O6JXFI0011292O12073"""
    PRDC_YM_NM: Union[str, int, float, None] = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: Union[str, int, float, None] = Field(None, description="공개파일명", alias="OPB_FL_NM")
    INST_CD: Union[str, int, float, None] = Field(None, description="기관코드", alias="INST_CD")
    INST_NM: Union[str, int, float, None] = Field(None, description="기관명", alias="INST_NM")
    OPB_FL_PH: Union[str, int, float, None] = Field(None, description="공개파일경로", alias="OPB_FL_PH")
    FILE_ID: Union[str, int, float, None] = Field(None, description="파일ID", alias="FILE_ID")

class Params_O6JXFI0011292O12073(BaseModel):
    """Request parameters for O6JXFI0011292O12073"""
    PRDC_YM_NM: str | None = Field(None, description="생산년월", alias="PRDC_YM_NM")
    OPB_FL_NM: str | None = Field(None, description="공개파일명", alias="OPB_FL_NM")
    INST_NM: str | None = Field(None, description="기관명", alias="INST_NM")

class Model_OKAPKX000929X915616(BaseModel):
    """Response model for OKAPKX000929X915616"""
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SBM: Union[str, int, float, None] = Field(None, description="제출(건)", alias="SBM")
    DEAL_CN_PSSG: Union[str, int, float, None] = Field(None, description="가결(건)", alias="DEAL_CN_PSSG")
    DEAL_CN_RJCTN: Union[str, int, float, None] = Field(None, description="부결(건)", alias="DEAL_CN_RJCTN")
    DEAL_CN_DSU: Union[str, int, float, None] = Field(None, description="폐기(건)", alias="DEAL_CN_DSU")
    DEAL_CN_WTHD: Union[str, int, float, None] = Field(None, description="철회(건)", alias="DEAL_CN_WTHD")
    DEAL_CN_GVB: Union[str, int, float, None] = Field(None, description="반려(건)", alias="DEAL_CN_GVB")
    DEAL_CN_RSVT: Union[str, int, float, None] = Field(None, description="보류(건)", alias="DEAL_CN_RSVT")
    TERM_EXPR_DSU: Union[str, int, float, None] = Field(None, description="임기만료폐기(건)", alias="TERM_EXPR_DSU")

class Params_OKAPKX000929X915616(BaseModel):
    """Request parameters for OKAPKX000929X915616"""
    ERACO: str | None = Field(None, description="대수", alias="ERACO")

class Model_O5VQRK0008587911609(BaseModel):
    """Response model for O5VQRK0008587911609"""
    YEAR: Union[str, int, float, None] = Field(None, description="연도", alias="YEAR")
    MAJR: Union[str, int, float, None] = Field(None, description="분야", alias="MAJR")
    ORG_NM: Union[str, int, float, None] = Field(None, description="단체", alias="ORG_NM")
    NOR_ENTERATM: Union[str, int, float, None] = Field(None, description="일반수용비(원)", alias="NOR_ENTERATM")
    BUS_GOATM: Union[str, int, float, None] = Field(None, description="사업추진비(원)", alias="BUS_GOATM")
    SPE_WORKATM: Union[str, int, float, None] = Field(None, description="특정업무경비(원)", alias="SPE_WORKATM")
    POLICY_RESRCH_ATM: Union[str, int, float, None] = Field(None, description="정책연구비(원)", alias="POLICY_RESRCH_ATM")

class Params_O5VQRK0008587911609(BaseModel):
    """Request parameters for O5VQRK0008587911609"""
    YEAR: str | None = Field(None, description="연도", alias="YEAR")
    MAJR: str | None = Field(None, description="분야", alias="MAJR")
    ORG_NM: str | None = Field(None, description="단체", alias="ORG_NM")

class Model_OOWY4R001216HX11495(BaseModel):
    """Response model for OOWY4R001216HX11495"""
    BDG_CONF_RSLT: Union[str, int, float, None] = Field(None, description="종합심사 회의결과", alias="BDG_CONF_RSLT")
    BDG_CONF_DT: Union[str, int, float, None] = Field(None, description="종합심사 회의일", alias="BDG_CONF_DT")
    BDG_CONF_NM: Union[str, int, float, None] = Field(None, description="종합심사 회의명", alias="BDG_CONF_NM")
    PPSL_DT: Union[str, int, float, None] = Field(None, description="제안일", alias="PPSL_DT")
    PPSR: Union[str, int, float, None] = Field(None, description="제안자", alias="PPSR")
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")

class Params_OOWY4R001216HX11495(BaseModel):
    """Request parameters for OOWY4R001216HX11495"""
    BILL_ID: str = Field(..., description="의안ID", alias="BILL_ID")

class Model_OOWY4R001216HX11471(BaseModel):
    """Response model for OOWY4R001216HX11471"""
    BIL_DIV_NM: Union[str, int, float, None] = Field(None, description="의안구분명", alias="BIL_DIV_NM")
    BIL_DIV_NM2: Union[str, int, float, None] = Field(None, description="의안구분명", alias="BIL_DIV_NM2")
    RCP_CNT: Union[str, int, float, None] = Field(None, description="접수건수", alias="RCP_CNT")
    PROC_CNT: Union[str, int, float, None] = Field(None, description="처리건수", alias="PROC_CNT")
    RSVT_CNT: Union[str, int, float, None] = Field(None, description="보류건수", alias="RSVT_CNT")

class Params_OOWY4R001216HX11471(BaseModel):
    """Request parameters for OOWY4R001216HX11471"""
    ERACO: str = Field(..., description="대수", alias="ERACO")

class Model_OOWY4R001216HX11521(BaseModel):
    """Response model for OOWY4R001216HX11521"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    FILE_CN: Union[str, int, float, None] = Field(None, description="파일설명", alias="FILE_CN")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11521(BaseModel):
    """Request parameters for OOWY4R001216HX11521"""
    CONF_ID: str | None = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: str | None = Field(None, description="대수", alias="ERACO")

class Model_O67B1I001080WL10254(BaseModel):
    """Response model for O67B1I001080WL10254"""
    TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="TITLE")
    LINK: Union[str, int, float, None] = Field(None, description="의원실링크", alias="LINK")
    DESCRIPTION: Union[str, int, float, None] = Field(None, description="설명", alias="DESCRIPTION")
    SDATE: Union[str, int, float, None] = Field(None, description="개최일", alias="SDATE")
    STIME: Union[str, int, float, None] = Field(None, description="개최시간", alias="STIME")
    NAME: Union[str, int, float, None] = Field(None, description="주최기관", alias="NAME")
    LOCATION: Union[str, int, float, None] = Field(None, description="개최장소", alias="LOCATION")

class Params_O67B1I001080WL10254(BaseModel):
    """Request parameters for O67B1I001080WL10254"""
    TITLE: str | None = Field(None, description="제목", alias="TITLE")
    DESCRIPTION: str | None = Field(None, description="설명", alias="DESCRIPTION")
    SDATE: str | None = Field(None, description="개최일", alias="SDATE")
    NAME: str | None = Field(None, description="주최기관", alias="NAME")
    LOCATION: str | None = Field(None, description="개최장소", alias="LOCATION")

class Model_OOWY4R001216HX11524(BaseModel):
    """Response model for OOWY4R001216HX11524"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    BLL_NO: Union[str, int, float, None] = Field(None, description="안건 번호", alias="BLL_NO")
    BLL_NM: Union[str, int, float, None] = Field(None, description="안건명", alias="BLL_NM")
    BLL_LV: Union[str, int, float, None] = Field(None, description="안건 레벨", alias="BLL_LV")

class Params_OOWY4R001216HX11524(BaseModel):
    """Request parameters for OOWY4R001216HX11524"""
    CONF_ID: str = Field(..., description="회의ID", alias="CONF_ID")

class Model_OHAC6C000892WC13765(BaseModel):
    """Response model for OHAC6C000892WC13765"""
    ORD_NUM: Union[str, int, float, None] = Field(None, description="대수", alias="ORD_NUM")
    YR: Union[str, int, float, None] = Field(None, description="연도", alias="YR")
    OPB_DAY: Union[str, int, float, None] = Field(None, description="공개날짜", alias="OPB_DAY")
    PN: Union[str, int, float, None] = Field(None, description="성명", alias="PN")
    CCOF_INST_NM: Union[str, int, float, None] = Field(None, description="겸직기관명", alias="CCOF_INST_NM")
    PSIT_NM: Union[str, int, float, None] = Field(None, description="직위", alias="PSIT_NM")
    CCOF_PSB_YN_CD: Union[str, int, float, None] = Field(None, description="결정 내용", alias="CCOF_PSB_YN_CD")

class Params_OHAC6C000892WC13765(BaseModel):
    """Request parameters for OHAC6C000892WC13765"""
    ORD_NUM: str | None = Field(None, description="대수", alias="ORD_NUM")
    YR: str | None = Field(None, description="연도", alias="YR")
    OPB_DAY: str | None = Field(None, description="공개날짜", alias="OPB_DAY")
    PN: str | None = Field(None, description="성명", alias="PN")
    CCOF_INST_NM: str | None = Field(None, description="겸직기관명", alias="CCOF_INST_NM")
    PSIT_NM: str | None = Field(None, description="직위", alias="PSIT_NM")

class Model_O8U5BW001076JT16522(BaseModel):
    """Response model for O8U5BW001076JT16522"""
    SEQ: Union[str, int, float, None] = Field(None, description="순번", alias="SEQ")
    DT: Union[str, int, float, None] = Field(None, description="일자", alias="DT")
    BILL_KIND: Union[str, int, float, None] = Field(None, description="의안구분", alias="BILL_KIND")
    AGE: Union[str, int, float, None] = Field(None, description="대수", alias="AGE")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NM: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NM")
    STAGE: Union[str, int, float, None] = Field(None, description="단계", alias="STAGE")
    DTL_STAGE: Union[str, int, float, None] = Field(None, description="세부단계", alias="DTL_STAGE")
    COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위원회", alias="COMMITTEE")
    ACT_STATUS: Union[str, int, float, None] = Field(None, description="활동상태", alias="ACT_STATUS")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크URL", alias="LINK_URL")
    COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위원회ID", alias="COMMITTEE_ID")

class Params_O8U5BW001076JT16522(BaseModel):
    """Request parameters for O8U5BW001076JT16522"""
    DT: str = Field(..., description="일자", alias="DT")
    BILL_KIND: str | None = Field(None, description="의안구분", alias="BILL_KIND")
    AGE: str = Field(..., description="대수", alias="AGE")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NM: str | None = Field(None, description="의안명", alias="BILL_NM")
    STAGE: str | None = Field(None, description="단계", alias="STAGE")
    DTL_STAGE: str | None = Field(None, description="세부단계", alias="DTL_STAGE")
    COMMITTEE: str | None = Field(None, description="소관위원회", alias="COMMITTEE")
    ACT_STATUS: str | None = Field(None, description="활동상태", alias="ACT_STATUS")
    BILL_ID: str | None = Field(None, description="의안ID", alias="BILL_ID")
    COMMITTEE_ID: str | None = Field(None, description="소관위원회ID", alias="COMMITTEE_ID")

class Model_OOWY4R001216HX11505(BaseModel):
    """Response model for OOWY4R001216HX11505"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    CONF_KND: Union[str, int, float, None] = Field(None, description="회의종류", alias="CONF_KND")
    CMIT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="CMIT_CD")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운로드 URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11505(BaseModel):
    """Request parameters for OOWY4R001216HX11505"""
    ERACO: str = Field(..., description="대수", alias="ERACO")
    CMIT_CD: str | None = Field(None, description="위원회코드", alias="CMIT_CD")

class Model_OFPR4Q001057VP11437(BaseModel):
    """Response model for OFPR4Q001057VP11437"""
    COMP_MAIN_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="COMP_MAIN_TITLE")
    REG_DATE: Union[str, int, float, None] = Field(None, description="등록일자", alias="REG_DATE")
    COMP_CONTENT: Union[str, int, float, None] = Field(None, description="내용", alias="COMP_CONTENT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="상세보기", alias="LINK_URL")

class Params_OFPR4Q001057VP11437(BaseModel):
    """Request parameters for OFPR4Q001057VP11437"""
    COMP_MAIN_TITLE: str | None = Field(None, description="제목", alias="COMP_MAIN_TITLE")
    COMP_CONTENT: str | None = Field(None, description="내용", alias="COMP_CONTENT")

class Model_OTM7PV000945R113521(BaseModel):
    """Response model for OTM7PV000945R113521"""
    CONTENTS: Union[str, int, float, None] = Field(None, description="내용", alias="CONTENTS")
    SCHEDULEDATE: Union[str, int, float, None] = Field(None, description="날짜", alias="SCHEDULEDATE")
    SCHEDULETIME: Union[str, int, float, None] = Field(None, description="시간", alias="SCHEDULETIME")

class Params_OTM7PV000945R113521(BaseModel):
    """Request parameters for OTM7PV000945R113521"""
    CONTENTS: str | None = Field(None, description="내용", alias="CONTENTS")
    SCHEDULEDATE: str | None = Field(None, description="날짜", alias="SCHEDULEDATE")
    SCHEDULETIME: str | None = Field(None, description="시간", alias="SCHEDULETIME")

class Model_OPR1MQ000998LC12535(BaseModel):
    """Response model for OPR1MQ000998LC12535"""
    HG_NM: Union[str, int, float, None] = Field(None, description="의원", alias="HG_NM")
    HJ_NM: Union[str, int, float, None] = Field(None, description="한자명", alias="HJ_NM")
    POLY_NM: Union[str, int, float, None] = Field(None, description="정당", alias="POLY_NM")
    ORIG_NM: Union[str, int, float, None] = Field(None, description="선거구", alias="ORIG_NM")
    MEMBER_NO: Union[str, int, float, None] = Field(None, description="의원번호", alias="MEMBER_NO")
    POLY_CD: Union[str, int, float, None] = Field(None, description="소속정당코드", alias="POLY_CD")
    ORIG_CD: Union[str, int, float, None] = Field(None, description="선거구코드", alias="ORIG_CD")
    VOTE_DATE: Union[str, int, float, None] = Field(None, description="의결일자", alias="VOTE_DATE")
    BILL_NO: Union[str, int, float, None] = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: Union[str, int, float, None] = Field(None, description="의안명", alias="BILL_NAME")
    BILL_ID: Union[str, int, float, None] = Field(None, description="의안ID", alias="BILL_ID")
    LAW_TITLE: Union[str, int, float, None] = Field(None, description="법률명", alias="LAW_TITLE")
    CURR_COMMITTEE: Union[str, int, float, None] = Field(None, description="소관위원회", alias="CURR_COMMITTEE")
    RESULT_VOTE_MOD: Union[str, int, float, None] = Field(None, description="표결결과", alias="RESULT_VOTE_MOD")
    DEPT_CD: Union[str, int, float, None] = Field(None, description="부서코드(사용안함)", alias="DEPT_CD")
    CURR_COMMITTEE_ID: Union[str, int, float, None] = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    DISP_ORDER: Union[str, int, float, None] = Field(None, description="표시정렬순서", alias="DISP_ORDER")
    BILL_URL: Union[str, int, float, None] = Field(None, description="의안URL", alias="BILL_URL")
    BILL_NAME_URL: Union[str, int, float, None] = Field(None, description="의안링크", alias="BILL_NAME_URL")
    SESSION_CD: Union[str, int, float, None] = Field(None, description="회기", alias="SESSION_CD")
    CURRENTS_CD: Union[str, int, float, None] = Field(None, description="차수", alias="CURRENTS_CD")
    AGE: Union[str, int, float, None] = Field(None, description="대", alias="AGE")
    MONA_CD: Union[str, int, float, None] = Field(None, description="국회의원코드", alias="MONA_CD")

class Params_OPR1MQ000998LC12535(BaseModel):
    """Request parameters for OPR1MQ000998LC12535"""
    HG_NM: str | None = Field(None, description="의원", alias="HG_NM")
    POLY_NM: str | None = Field(None, description="정당", alias="POLY_NM")
    MEMBER_NO: str | None = Field(None, description="의원번호", alias="MEMBER_NO")
    VOTE_DATE: str | None = Field(None, description="의결일자", alias="VOTE_DATE")
    BILL_NO: str | None = Field(None, description="의안번호", alias="BILL_NO")
    BILL_NAME: str | None = Field(None, description="의안명", alias="BILL_NAME")
    BILL_ID: str = Field(..., description="의안ID", alias="BILL_ID")
    CURR_COMMITTEE: str | None = Field(None, description="소관위원회", alias="CURR_COMMITTEE")
    RESULT_VOTE_MOD: str | None = Field(None, description="표결결과", alias="RESULT_VOTE_MOD")
    CURR_COMMITTEE_ID: str | None = Field(None, description="소관위코드", alias="CURR_COMMITTEE_ID")
    MONA_CD: str | None = Field(None, description="국회의원코드", alias="MONA_CD")
    AGE: str = Field(..., description="대", alias="AGE")

class Model_O3VXPE000987AB14703(BaseModel):
    """Response model for O3VXPE000987AB14703"""
    V_TITLE: Union[str, int, float, None] = Field(None, description="제목", alias="V_TITLE")
    URL_LINK: Union[str, int, float, None] = Field(None, description="기사 URL", alias="URL_LINK")
    DATE_LASTMODIFIED: Union[str, int, float, None] = Field(None, description="최종수정일", alias="DATE_LASTMODIFIED")
    DATE_RELEASED: Union[str, int, float, None] = Field(None, description="기사작성일", alias="DATE_RELEASED")
    V_BODY: Union[str, int, float, None] = Field(None, description="기사내용", alias="V_BODY")

class Params_O3VXPE000987AB14703(BaseModel):
    """Request parameters for O3VXPE000987AB14703"""
    V_TITLE: str | None = Field(None, description="제목", alias="V_TITLE")

class Model_OOWY4R001216HX11511(BaseModel):
    """Response model for OOWY4R001216HX11511"""
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    CONF_KND: Union[str, int, float, None] = Field(None, description="회의종류", alias="CONF_KND")
    CMIT_CD: Union[str, int, float, None] = Field(None, description="위원회코드", alias="CMIT_CD")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운로드 URL", alias="DOWN_URL")

class Params_OOWY4R001216HX11511(BaseModel):
    """Request parameters for OOWY4R001216HX11511"""
    ERACO: str = Field(..., description="대수", alias="ERACO")
    CMIT_CD: str | None = Field(None, description="위원회코드", alias="CMIT_CD")

class Model_O3YBRH0011715419177(BaseModel):
    """Response model for O3YBRH0011715419177"""
    REG_DATE: Union[str, int, float, None] = Field(None, description="발간일", alias="REG_DATE")
    DEPARTMENT_NAME: Union[str, int, float, None] = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: Union[str, int, float, None] = Field(None, description="보고서명", alias="SUBJECT")
    LINK_URL: Union[str, int, float, None] = Field(None, description="링크 주소", alias="LINK_URL")

class Params_O3YBRH0011715419177(BaseModel):
    """Request parameters for O3YBRH0011715419177"""
    DEPARTMENT_NAME: str | None = Field(None, description="부서명", alias="DEPARTMENT_NAME")
    SUBJECT: str | None = Field(None, description="보고서명", alias="SUBJECT")

class Model_OWKPDF000891EB10683(BaseModel):
    """Response model for OWKPDF000891EB10683"""
    DIV_NM: Union[str, int, float, None] = Field(None, description="구분", alias="DIV_NM")
    ADDR: Union[str, int, float, None] = Field(None, description="주소", alias="ADDR")
    ARE: Union[str, int, float, None] = Field(None, description="면적(㎡)", alias="ARE")
    FLSP: Union[str, int, float, None] = Field(None, description="면적(평)", alias="FLSP")
    AMT: Union[str, int, float, None] = Field(None, description="금액", alias="AMT")
    YR: Union[str, int, float, None] = Field(None, description="년도", alias="YR")

class Params_OWKPDF000891EB10683(BaseModel):
    """Request parameters for OWKPDF000891EB10683"""
    DIV_NM: str | None = Field(None, description="구분", alias="DIV_NM")
    ADDR: str | None = Field(None, description="주소", alias="ADDR")
    YR: str | None = Field(None, description="년도", alias="YR")

class Model_OOWY4R001216HX11416(BaseModel):
    """Response model for OOWY4R001216HX11416"""
    RPT_YR: Union[str, int, float, None] = Field(None, description="보고서 년도", alias="RPT_YR")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    RPT_TTL: Union[str, int, float, None] = Field(None, description="보고서 제목", alias="RPT_TTL")
    PDF_DWLD_URL: Union[str, int, float, None] = Field(None, description="PDF 다운 URL", alias="PDF_DWLD_URL")
    HWP_DWLD_URL: Union[str, int, float, None] = Field(None, description="HWP 다운 URL", alias="HWP_DWLD_URL")

class Params_OOWY4R001216HX11416(BaseModel):
    """Request parameters for OOWY4R001216HX11416"""
    RPT_YR: str | None = Field(None, description="보고서 년도", alias="RPT_YR")
    RPT_TTL: str | None = Field(None, description="보고서 제목", alias="RPT_TTL")

class Model_OOWY4R001216HX11516(BaseModel):
    """Response model for OOWY4R001216HX11516"""
    CONF_KND: Union[str, int, float, None] = Field(None, description="회의종류", alias="CONF_KND")
    ERACO: Union[str, int, float, None] = Field(None, description="대수", alias="ERACO")
    SESS: Union[str, int, float, None] = Field(None, description="회기", alias="SESS")
    DGR: Union[str, int, float, None] = Field(None, description="차수", alias="DGR")
    CONF_DT: Union[str, int, float, None] = Field(None, description="회의일자", alias="CONF_DT")
    CONF_ID: Union[str, int, float, None] = Field(None, description="회의ID", alias="CONF_ID")
    FILE_KND: Union[str, int, float, None] = Field(None, description="파일종류", alias="FILE_KND")
    FILE_CN: Union[str, int, float, None] = Field(None, description="파일설명", alias="FILE_CN")
    DOWN_URL: Union[str, int, float, None] = Field(None, description="다운URL", alias="DOWN_URL")
    CONFER_NUM: Union[str, int, float, None] = Field(None, description="회의번호", alias="CONFER_NUM")

class Params_OOWY4R001216HX11516(BaseModel):
    """Request parameters for OOWY4R001216HX11516"""
    CONF_ID: str = Field(..., description="회의ID", alias="CONF_ID")

class Model_OOWY4R001216HX11439(BaseModel):
    """Response model for OOWY4R001216HX11439"""
    NAAS_CD: Union[str, int, float, None] = Field(None, description="국회의원코드", alias="NAAS_CD")
    NAAS_NM: Union[str, int, float, None] = Field(None, description="국회의원명", alias="NAAS_NM")
    NAAS_CH_NM: Union[str, int, float, None] = Field(None, description="국회의원한자명", alias="NAAS_CH_NM")
    NAAS_EN_NM: Union[str, int, float, None] = Field(None, description="국회의원영문명", alias="NAAS_EN_NM")
    BIRDY_DIV_CD: Union[str, int, float, None] = Field(None, description="생일구분코드", alias="BIRDY_DIV_CD")
    BIRDY_DT: Union[str, int, float, None] = Field(None, description="생일일자", alias="BIRDY_DT")
    DTY_NM: Union[str, int, float, None] = Field(None, description="직책명", alias="DTY_NM")
    PLPT_NM: Union[str, int, float, None] = Field(None, description="정당명", alias="PLPT_NM")
    ELECD_NM: Union[str, int, float, None] = Field(None, description="선거구명", alias="ELECD_NM")
    ELECD_DIV_NM: Union[str, int, float, None] = Field(None, description="선거구구분명", alias="ELECD_DIV_NM")
    CMIT_NM: Union[str, int, float, None] = Field(None, description="위원회명", alias="CMIT_NM")
    BLNG_CMIT_NM: Union[str, int, float, None] = Field(None, description="소속위원회명", alias="BLNG_CMIT_NM")
    RLCT_DIV_NM: Union[str, int, float, None] = Field(None, description="재선구분명", alias="RLCT_DIV_NM")
    GTELT_ERACO: Union[str, int, float, None] = Field(None, description="당선대수", alias="GTELT_ERACO")
    NTR_DIV: Union[str, int, float, None] = Field(None, description="성별", alias="NTR_DIV")
    NAAS_TEL_NO: Union[str, int, float, None] = Field(None, description="전화번호", alias="NAAS_TEL_NO")
    NAAS_EMAIL_ADDR: Union[str, int, float, None] = Field(None, description="국회의원이메일주소", alias="NAAS_EMAIL_ADDR")
    NAAS_HP_URL: Union[str, int, float, None] = Field(None, description="국회의원홈페이지URL", alias="NAAS_HP_URL")
    AIDE_NM: Union[str, int, float, None] = Field(None, description="보좌관", alias="AIDE_NM")
    CHF_SCRT_NM: Union[str, int, float, None] = Field(None, description="비서관", alias="CHF_SCRT_NM")
    SCRT_NM: Union[str, int, float, None] = Field(None, description="비서", alias="SCRT_NM")
    BRF_HST: Union[str, int, float, None] = Field(None, description="약력", alias="BRF_HST")
    OFFM_RNUM_NO: Union[str, int, float, None] = Field(None, description="사무실 호실", alias="OFFM_RNUM_NO")
    NAAS_PIC: Union[str, int, float, None] = Field(None, description="국회의원사진", alias="NAAS_PIC")

class Params_OOWY4R001216HX11439(BaseModel):
    """Request parameters for OOWY4R001216HX11439"""
    NAAS_CD: str | None = Field(None, description="국회의원코드", alias="NAAS_CD")
    NAAS_NM: str | None = Field(None, description="국회의원명", alias="NAAS_NM")
    PLPT_NM: str | None = Field(None, description="정당명", alias="PLPT_NM")
    BLNG_CMIT_NM: str | None = Field(None, description="소속위원회명", alias="BLNG_CMIT_NM")

class Model_O7FHUO000928X018370(BaseModel):
    """Response model for O7FHUO000928X018370"""
    ORD_NO: Union[str, int, float, None] = Field(None, description="대수", alias="ORD_NO")
    PLPT_NM: Union[str, int, float, None] = Field(None, description="정당 / 단체", alias="PLPT_NM")
    NFVP_RT: Union[str, int, float, None] = Field(None, description="득표율", alias="NFVP_RT")
    PLMST_PSNCNT: Union[str, int, float, None] = Field(None, description="의석수", alias="PLMST_PSNCNT")
    PRPRR_PSNCNT: Union[str, int, float, None] = Field(None, description="비례대표수", alias="PRPRR_PSNCNT")

class Params_O7FHUO000928X018370(BaseModel):
    """Request parameters for O7FHUO000928X018370"""
    ORD_NO: str | None = Field(None, description="대수", alias="ORD_NO")
    PLPT_NM: str | None = Field(None, description="정당 / 단체", alias="PLPT_NM")
