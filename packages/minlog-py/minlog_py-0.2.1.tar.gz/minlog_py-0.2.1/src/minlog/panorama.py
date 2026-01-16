import base64
import json
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Attachment:
    name: str
    contentType: str
    body: str  # Base64 or plain text


@dataclass
class LogStep:
    title: str
    status: str = "passed"  # passed, failed, skipped
    startTime: float = field(default_factory=time.time)
    duration: float = 0
    attachments: List[Attachment] = field(default_factory=list)
    error: Optional[str] = None
    steps: List["LogStep"] = field(default_factory=list)

    def end(self):
        self.duration = (time.time() - self.startTime) * 1000  # ms


@dataclass
class LogSuite:
    title: str
    status: str = "passed"
    startTime: float = field(default_factory=time.time)
    duration: float = 0
    steps: List[LogStep] = field(default_factory=list)

    def end(self):
        self.duration = (time.time() - self.startTime) * 1000
        # Determine status based on steps
        if any(s.status == "failed" for s in self.steps):
            self.status = "failed"


class PanoramaReport:
    def __init__(self, title: str = "MinLog Panorama Report"):
        self.title = title
        self.startTime = datetime.now().isoformat()
        self.suites: List[LogSuite] = []
        self._current_suite: Optional[LogSuite] = None
        self._step_stack: List[LogStep] = []

    def start_suite(self, title: str):
        suite = LogSuite(title=title)
        self.suites.append(suite)
        self._current_suite = suite
        return suite

    def end_suite(self):
        if self._current_suite:
            self._current_suite.end()
            self._current_suite = None

    def start_step(self, title: str):
        step = LogStep(title=title)
        if self._step_stack:
            self._step_stack[-1].steps.append(step)
        elif self._current_suite:
            self._current_suite.steps.append(step)

        self._step_stack.append(step)
        return step

    def end_step(self, status: str = "passed", error: str = None):
        if self._step_stack:
            step = self._step_stack.pop()
            step.status = status
            step.error = error
            step.end()
            return step

    def add_attachment(self, name: str, content: Any, content_type: str = "text/plain"):
        if not self._step_stack:
            return

        if isinstance(content, (dict, list)):
            body = json.dumps(content, indent=2)
            content_type = "application/json"
        elif isinstance(content, bytes):
            body = base64.b64encode(content).decode("utf-8")
        else:
            body = str(content)

        attachment = Attachment(name=name, contentType=content_type, body=body)
        self._step_stack[-1].attachments.append(attachment)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "meta": {"title": self.title, "startTime": self.startTime, "generatedAt": datetime.now().isoformat()},
            "suites": [asdict(s) for s in self.suites],
        }

    def save_html(self, output_path: str, template_path: Optional[str] = None):
        data_json = json.dumps(self.to_dict(), ensure_ascii=False)

        if template_path and Path(template_path).exists():
            template = Path(template_path).read_text(encoding="utf-8")
        else:
            # Fallback to internal default template finder/logic
            from .viewer_template import DEFAULT_TEMPLATE

            template = DEFAULT_TEMPLATE

        html_content = template.replace("window.LOG_PAYLOAD = null;", f"window.LOG_PAYLOAD = {data_json};")

        Path(output_path).write_text(html_content, encoding="utf-8")
        print(f"[MinLog] Panorama report saved to: {output_path}")
