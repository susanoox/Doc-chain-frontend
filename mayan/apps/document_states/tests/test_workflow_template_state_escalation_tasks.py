from mayan.apps.documents.tests.base import GenericDocumentTestCase

from ..events import event_workflow_instance_transitioned

from .mixins.workflow_template_state_escalation_mixins import WorkflowTemplateStateEscalationTaskTestMixin


class WorkflowTemplateStateEscalationTaskTestCase(
    WorkflowTemplateStateEscalationTaskTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self._create_test_workflow_template_state_escalation(
            extra_kwargs={'unit': 'microseconds'}
        )
        self._create_test_document_stub()

    def test_task_workflow_instance_check_escalation(self):
        test_workflow_instance = self._test_document.workflows.first()
        test_workflow_instance_state = test_workflow_instance.get_current_state()

        self._clear_events()

        self._execute_task_workflow_instance_check_escalation(
            test_workflow_instance_id=test_workflow_instance.pk
        )

        self.assertNotEqual(
            test_workflow_instance.get_current_state(),
            test_workflow_instance_state
        )
        self.assertEqual(
            test_workflow_instance.get_last_log_entry().comment,
            self._test_workflow_template_state_escalation.comment
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(
            events[0].actor, self._test_document.workflows.first()
        )
        self.assertEqual(
            events[0].target, self._test_document.workflows.first()
        )
        self.assertEqual(
            events[0].verb, event_workflow_instance_transitioned.id
        )

    def test_task_workflow_instance_check_escalation_all(self):
        test_workflow_instance = self._test_document.workflows.first()
        test_workflow_instance_state = test_workflow_instance.get_current_state()

        self._clear_events()

        self._execute_task_workflow_instance_check_escalation_all()

        self.assertNotEqual(
            test_workflow_instance.get_current_state(),
            test_workflow_instance_state
        )
        self.assertEqual(
            test_workflow_instance.get_last_log_entry().comment,
            self._test_workflow_template_state_escalation.comment
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(
            events[0].actor, self._test_document.workflows.first()
        )
        self.assertEqual(
            events[0].target, self._test_document.workflows.first()
        )
        self.assertEqual(
            events[0].verb, event_workflow_instance_transitioned.id
        )
